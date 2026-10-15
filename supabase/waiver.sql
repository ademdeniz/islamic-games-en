-- Youth Gathering waiver (parent sign-off) – database setup for the same Supabase project.
-- Run once in Supabase: Dashboard → SQL Editor → New query → paste this whole file → Run.
-- Needs schema.sql to be installed first (it uses public.my_role() to know who is the admin).
-- Safe to re-run, and it keeps working if schema.sql is re-run later.
--
-- Parents are not logged in: the public waiver page can only call submit_waiver(), which checks every
-- field and saves one row. Nobody but an admin can read, and only an admin can delete (duplicates, tests).

create extension if not exists pgcrypto;

create table if not exists public.trip_waivers (
  id                 uuid primary key default gen_random_uuid(),
  event              text not null,
  parent_first       text not null,
  parent_last        text not null,
  parent_email       text not null,
  parent_phone       text not null,
  relationship       text not null check (relationship in ('Mother', 'Father', 'Legal guardian')),
  children           jsonb not null,           -- [{first, last, birth_date, gender, medical}]
  emergency_name     text not null,
  emergency_phone    text not null,
  photo_consent      boolean not null,
  acknowledgements   jsonb not null,           -- the statements the parent ticked, word for word
  signature_name     text not null,
  signature_image    text not null,            -- PNG data URL of the drawn signature
  user_agent         text,
  signed_at          timestamptz not null default now()
);
create index if not exists trip_waivers_event on public.trip_waivers (event, signed_at desc);

alter table public.trip_waivers enable row level security;

drop policy if exists "admin reads waivers" on public.trip_waivers;
create policy "admin reads waivers" on public.trip_waivers for select to authenticated
  using (public.my_role() = 'admin');
drop policy if exists "admin deletes waivers" on public.trip_waivers;
create policy "admin deletes waivers" on public.trip_waivers for delete to authenticated
  using (public.my_role() = 'admin');

revoke all on public.trip_waivers from anon, authenticated;
grant select, delete on public.trip_waivers to authenticated;

-- ------------------------------------------------------------------ the only way in
create or replace function public.submit_waiver(p jsonb) returns uuid
language plpgsql security definer set search_path = public as $$
declare
  c jsonb;
  t text;
  new_id uuid;
  email_re constant text := '^[^@\s]+@[^@\s]+\.[^@\s]+$';
begin
  if coalesce(p ->> 'event', '') !~ '^[a-z0-9-]{3,60}$' then raise exception 'Unknown event.'; end if;
  foreach t in array array['parent_first', 'parent_last', 'parent_email', 'parent_phone',
                           'emergency_name', 'emergency_phone', 'signature_name'] loop
    if length(trim(coalesce(p ->> t, ''))) not between 2 and 120 then
      raise exception 'Please fill in every required field (%).', t;
    end if;
  end loop;
  if trim(p ->> 'parent_email') !~ email_re then raise exception 'Please enter a valid e-mail address.'; end if;
  if length(regexp_replace(p ->> 'parent_phone', '\D', '', 'g')) < 7
     or length(regexp_replace(p ->> 'emergency_phone', '\D', '', 'g')) < 7 then
    raise exception 'Please enter a full phone number.';
  end if;
  if coalesce(p ->> 'relationship', '') not in ('Mother', 'Father', 'Legal guardian') then
    raise exception 'Please choose your relationship to the child.';
  end if;
  if coalesce((p ->> 'is_adult_guardian')::boolean, false) is not true then
    raise exception 'Only a parent or legal guardian aged 18 or over can sign.';
  end if;
  if jsonb_typeof(p -> 'photo_consent') is distinct from 'boolean' then
    raise exception 'Please answer the photo question.';
  end if;
  if jsonb_typeof(p -> 'acknowledgements') is distinct from 'array'
     or jsonb_array_length(p -> 'acknowledgements') not between 1 and 20 then
    raise exception 'Please tick every statement.';
  end if;
  if jsonb_typeof(p -> 'children') is distinct from 'array'
     or jsonb_array_length(p -> 'children') not between 1 and 8 then
    raise exception 'Add at least one child.';
  end if;
  for c in select * from jsonb_array_elements(p -> 'children') loop
    if length(trim(coalesce(c ->> 'first', ''))) not between 1 and 80
       or length(trim(coalesce(c ->> 'last', ''))) not between 1 and 80
       or coalesce(c ->> 'gender', '') not in ('Boy', 'Girl')
       or coalesce(c ->> 'birth_date', '') !~ '^\d{4}-\d{2}-\d{2}$'
       or length(coalesce(c ->> 'medical', '')) > 1000 then
      raise exception 'Please complete each child''s name, date of birth and boy/girl.';
    end if;
  end loop;
  if coalesce(p ->> 'signature_image', '') !~ '^data:image/png;base64,'
     or length(p ->> 'signature_image') > 200000 then
    raise exception 'Please draw your signature.';
  end if;

  insert into public.trip_waivers (event, parent_first, parent_last, parent_email, parent_phone, relationship,
    children, emergency_name, emergency_phone, photo_consent, acknowledgements, signature_name,
    signature_image, user_agent)
  values (p ->> 'event', trim(p ->> 'parent_first'), trim(p ->> 'parent_last'), lower(trim(p ->> 'parent_email')),
    trim(p ->> 'parent_phone'), p ->> 'relationship', p -> 'children', trim(p ->> 'emergency_name'),
    trim(p ->> 'emergency_phone'), (p ->> 'photo_consent')::boolean, p -> 'acknowledgements',
    trim(p ->> 'signature_name'), p ->> 'signature_image', left(p ->> 'user_agent', 300))
  returning id into new_id;
  return new_id;
end $$;

revoke execute on function public.submit_waiver(jsonb) from public;
grant execute on function public.submit_waiver(jsonb) to anon, authenticated;
