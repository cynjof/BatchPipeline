from airflow.models import DagBag


def test_no_import_errors(monkeypatch):

    # Set variables
    monkeypatch.setenv("AIRFLOW_VAR_BUCKET", "test-bucket")
    monkeypatch.setenv("AIRFLOW_VAR_EMR_ID", "test-emr-id")

    # Testing
    dag_bag = DagBag()
    assert dag is not None, f'DAG not found in DagBag'
    assert len(dag_bag.import_errors) == 0, "No Import Failures"
    assert 1==2