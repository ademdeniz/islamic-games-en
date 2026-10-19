"""The homework check: every weekly update has a checklist (updates/<Sunday>/homework.json) whose tasks point at real
pages, with the minimum minutes from data/homework.json, keyed the way the tracker records visits."""
import glob
import importlib.util
import json
import os

from conftest import ROOT

spec = importlib.util.spec_from_file_location('build_update', os.path.join(ROOT, 'tools', 'build_update.py'))
bu = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bu)
MIN = json.load(open(os.path.join(ROOT, 'data', 'homework.json')))
DAYS = sorted(os.path.basename(f)[:-5] for f in glob.glob(os.path.join(ROOT, 'data', 'updates', '*.json')))


def page_exists(key):
    path = key.split('#')[0]
    return os.path.exists(os.path.join(ROOT, path, 'index.html'))


def test_every_update_has_a_checklist_for_every_group():
    assert DAYS
    for d in DAYS:
        hw = json.load(open(os.path.join(ROOT, 'updates', d, 'homework.json'), encoding='utf-8'))
        assert hw['week'] == d
        assert set(hw['groups']) == set(bu.GROUPS), d
        for g, tasks in hw['groups'].items():
            assert tasks, (d, g)
            ids = [t['id'] for t in tasks]
            assert len(ids) == len(set(ids)), (d, g, ids)


def test_tasks_point_at_real_pages_with_the_right_minimums():
    for d in DAYS:
        hw = json.load(open(os.path.join(ROOT, 'updates', d, 'homework.json'), encoding='utf-8'))
        for g, tasks in hw['groups'].items():
            for t in tasks:
                assert t['keys'] and all(page_exists(k) for k in t['keys']), (d, g, t)
                assert t['min'] == MIN[{'game': 'games'}.get(t['kind'], t['kind'])], t
                assert t['url'].startswith(bu.SITE), t
                if t['kind'] == 'quran':
                    assert t['keys'][0].startswith('games/citaj-kuran#page-') and t['url'].endswith(t['keys'][0]), t


def test_keys_are_what_the_tracker_records():
    assert bu.task_key(bu.SITE + 'lessons/ilmihal-2/17-messengers/') == 'lessons/ilmihal-2/17-messengers'
    assert bu.task_key(bu.SITE + 'games/learn-surahs-by-heart/#kafirun') == 'games/learn-surahs-by-heart#kafirun'
    assert bu.task_key(bu.SITE + 'sufara/rule-sukun/index.html') == 'sufara/rule-sukun'


def test_new_updates_show_last_weeks_homework_live_without_names():
    block = bu.homework_summary_html('2026-10-18')
    assert 'homework_summary' in block and 'W="2026-10-18"' in block and "'/homework.json'" in block and 'no names' in block


def test_read_along_and_surahs_put_the_page_in_the_address():
    ra = open(os.path.join(ROOT, 'games', 'citaj-kuran', 'index.html'), encoding='utf-8').read()
    hz = open(os.path.join(ROOT, 'games', 'learn-surahs-by-heart', 'index.html'), encoding='utf-8').read()
    assert "mark('#page-'+page().mushaf_page)" in ra and "'#page-'+p.mushaf_page===location.hash" in ra
    assert "history.replaceState(null,'','#'+DATA.surahs[k].id)" in hz
