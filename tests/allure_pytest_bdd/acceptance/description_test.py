import pytest
from hamcrest import assert_that
from hamcrest import equal_to

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_description
from allure_commons_test.result import has_description_html

from tests.allure_pytest.pytest_runner import AllurePytestRunner
from tests.e2e import version_lt


def test_description_decorator(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo

            This will be overwritten by code

            Scenario: Bar

                This will be overwritten by code

                Given noop
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenario, given
        import allure

        @allure.description("Lorem Ipsum")
        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @given("noop")
        def given_noop():
            pass
        """
    )

    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        steps_content,
    )

    assert_that(
        allure_results,
        has_test_case(
            "sample.feature:Bar",
            has_description(
                equal_to("Lorem Ipsum"),
            )
        )
    )


def test_description_at_module_level(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given noop
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenarios, given
        import allure

        pytestmark = [allure.description("Lorem Ipsum")]

        scenarios("sample.feature")

        @given("noop")
        def given_noop():
            pass
        """
    )

    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        steps_content,
    )

    assert_that(
        allure_results,
        has_test_case(
            "sample.feature:Bar",
            has_description(
                equal_to("Lorem Ipsum"),
            )
        )
    )


def test_description_html_decorator(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given noop
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenario, given
        import allure

        @allure.description_html("Lorem Ipsum")
        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @given("noop")
        def given_noop():
            pass
        """
    )

    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        steps_content,
    )

    assert_that(
        allure_results,
        has_test_case(
            "sample.feature:Bar",
            has_description_html(
                equal_to("Lorem Ipsum"),
            )
        )
    )


def test_description_html_decorator_at_module_level(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given noop
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenarios, given
        import allure

        pytestmark = [allure.description_html("Lorem Ipsum")]

        scenarios("sample.feature")

        @given("noop")
        def given_noop():
            pass
        """
    )

    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        steps_content,
    )

    assert_that(
        allure_results,
        has_test_case(
            "sample.feature:Bar",
            has_description_html(
                equal_to("Lorem Ipsum"),
            )
        )
    )


def test_dynamic_description(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo

            This will be overwritten by code

            Scenario: Bar

                This will be overwritten by code

                Given noop
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenario, given
        import allure

        @allure.description("This will be overwritten by the runtime API")
        @scenario("sample.feature", "Bar")
        def test_scenario():
            allure.dynamic.description("Lorem Ipsum")

        @given("noop")
        def given_noop():
            pass
        """
    )

    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        steps_content,
    )

    assert_that(
        allure_results,
        has_test_case(
            "sample.feature:Bar",
            has_description(
                equal_to("Lorem Ipsum"),
            )
        )
    )


def test_dynamic_description_html(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given noop
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenario, given
        import allure

        @allure.description_html("This will be overwritten by the runtime API")
        @scenario("sample.feature", "Bar")
        def test_scenario():
            allure.dynamic.description_html("Lorem Ipsum")

        @given("noop")
        def given_noop():
            pass
        """
    )

    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        steps_content,
    )

    assert_that(
        allure_results,
        has_test_case(
            "sample.feature:Bar",
            has_description_html(
                equal_to("Lorem Ipsum"),
            )
        )
    )


@pytest.mark.skipif(
    version_lt("pytest_bdd", 7),
    reason="Pytest-BDD doesn't support scenario-level descriptions until v7",
)
def test_scenario_description(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar

                Lorem Ipsum

                Given noop
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenario, given

        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @given("noop")
        def given_noop():
            pass
        """
    )

    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        steps_content,
    )

    assert_that(
        allure_results,
        has_test_case(
            "sample.feature:Bar",
            has_description(
                equal_to("Lorem Ipsum"),
            )
        )
    )


def test_feature_description(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo

            Lorem Ipsum

            Scenario: Bar

                Given noop
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenario, given

        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @given("noop")
        def given_noop():
            pass
        """
    )

    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        steps_content,
    )

    assert_that(
        allure_results,
        has_test_case(
            "sample.feature:Bar",
            has_description(
                equal_to("Lorem Ipsum"),
            )
        )
    )


@pytest.mark.skipif(
    version_lt("pytest_bdd", 7),
    reason="Pytest-BDD doesn't support scenario-level descriptions until v7",
)
def test_feature_and_scenario_description(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo

            Lorem Ipsum

            Scenario: Bar

                Dolor Sit Amet

                Given noop
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenario, given

        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @given("noop")
        def given_noop():
            pass
        """
    )

    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        steps_content,
    )

    assert_that(
        allure_results,
        has_test_case(
            "sample.feature:Bar",
            has_description(
                equal_to("Lorem Ipsum\n\nDolor Sit Amet"),
            )
        )
    )
