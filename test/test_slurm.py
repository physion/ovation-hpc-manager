import hpc_manager.slurm as slurm


def test_submit_research_job_throws_message_exception_for_missing_attributes():
    try:
        slurm.submit_research_job({})
        assert False, "Should throw exception"
    except slurm.MessageException as ex:
        assert str(ex) == "Missing required message attributes"


def test_submit_research_job_should_submit_batch():
    assert False
