import pytest
from airflow.models import DagBag


@pytest.fixture()
def dagbag():
    return DagBag()


def test_no_import_errors(monkeypatch):

    # Set variables
    monkeypatch.setenv("AIRFLOW_VAR_BUCKET", "test-bucket")
    monkeypatch.setenv("AIRFLOW_VAR_EMR_ID", "test-emr-id")

    dag_bag = dagbag()
    assert len(dag_bag.import_errors) == 0, "No Import Failures"
    assert dag_bag.size() == 1