# -*- encoding: utf-8 -*-

import uuid
from datetime import datetime, timezone
from typing import List, Optional, Union

from datahub.api.entities.datajob import DataJob
from datahub.utilities.urns.data_flow_urn import DataFlowUrn
from datahub.utilities.urns.data_job_urn import DataJobUrn
from datahub.utilities.urns.dataset_urn import DatasetUrn
from datahub.api.entities.dataprocess.dataprocess_instance import (
    DataProcessInstance, InstanceRunResult)

from metadata.entity.task import Task


class TaskMixin:

    def prepare_job(self, task: Task):
        datajob = DataJob(
            id=task.id,
            name=task.name,
            flow_urn=DataFlowUrn.create_from_string(task.workflow),
            properties=task.properties,
            url=task.url,
            tags=task.tags,
            owners=task.owners or {self.context.user_email},
            upstream_urns=[DataJobUrn.create_from_string(urn) for urn in (task.upstream_urns or [])],
            description=task.description,
        )
        return datajob

    def begin_job(self, datajob: DataJob, *, inputs: Optional[List[Union[str, DatasetUrn]]]=None):
        emitter = self.context.emitter
        datajob.inlets = [DatasetUrn.create_from_string(str(urn)) for urn in (inputs or [])]
        datajob.emit(emitter)
        run = DataProcessInstance.from_datajob(datajob=datajob, id=uuid.uuid4().hex)
        run.emit_process_start(emitter, int(
            datetime.now(timezone.utc).timestamp() * 1000))
        return run

    def end_job(self, run: DataProcessInstance, success=True, *, outputs: Optional[List[Union[str, DatasetUrn]]]=None):
        emitter = self.context.emitter
        datajob = run._template_object
        datajob.outlets = [DatasetUrn.create_from_string(str(urn)) for urn in (outputs or [])]
        datajob.emit(emitter)
        run.emit_process_end(emitter, int(datetime.now(
            timezone.utc).timestamp() * 1000), result=InstanceRunResult.SUCCESS if success else InstanceRunResult.FAILURE)
