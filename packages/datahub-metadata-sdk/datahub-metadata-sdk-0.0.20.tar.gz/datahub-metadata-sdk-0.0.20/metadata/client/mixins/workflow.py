# -*- encoding: utf-8 -*-

import uuid
from datetime import datetime, timezone

from datahub.api.entities.datajob import DataFlow
from datahub.api.entities.dataprocess.dataprocess_instance import (
    DataProcessInstance, InstanceRunResult)

from metadata.entity.workflow import Workflow


class WorkflowMixin:

    def prepare_workflow(self, workflow: Workflow):
        dataflow = DataFlow(
            id=workflow.id,
            name=workflow.name,
            orchestrator=workflow.orchestrator,
            cluster=self.context.env,
            properties=workflow.properties,
            url=workflow.url,
            tags=workflow.tags,
            owners=workflow.owners or {self.context.user_email},
        )
        return dataflow

    def begin_workflow(self, dataflow: DataFlow):
        emitter = self.context.emitter
        dataflow.emit(emitter)
        run = DataProcessInstance.from_dataflow(
            dataflow=dataflow, id=uuid.uuid4().hex)
        run.emit_process_start(emitter, int(
            datetime.now(timezone.utc).timestamp() * 1000))
        return run

    def end_workflow(self, run: DataProcessInstance, success=True):
        emitter = self.context.emitter
        run.emit_process_end(emitter, int(datetime.now(
            timezone.utc).timestamp() * 1000), result=InstanceRunResult.SUCCESS if success else InstanceRunResult.FAILURE)
