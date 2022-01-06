from bite_di import guard, Container


def test_no_issues():
    result = guard.run('tests.bite_di.no_issues_app', Container())
    assert result.success

