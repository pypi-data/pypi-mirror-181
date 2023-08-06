#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from poppy.core.db.base import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship
from poppy.core.db.non_null_column import NonNullColumn
from sqlalchemy.dialects.postgresql import BIGINT, INTEGER, ENUM, UUID, \
    TIMESTAMP

__all__ = ['JobLog',
           'JobException',
           'job_state_list',
           'job_status_list',
           'exception_level_list',
           'exception_type_list']

job_state_list = ['Pending', 'Terminated', 'Running']
job_status_list = ['OK', 'WARNING', 'ERROR']

job_state_enum = ENUM(*job_state_list,
                             name='job_state_type',
                      schema='poppy',
                      )
job_status_enum = ENUM(*job_status_list, name='job_status_type', schema='poppy')


class JobLog(Base):
    """
    The "job_log" table stores a log of the tasks’ jobs executed in
    the pipeline.
    """

    id_job_log = NonNullColumn(BIGINT(), primary_key=True)
    job_plugin = NonNullColumn(String(256), descr='Name of the plugin')
    job_task = NonNullColumn(String(256), descr='Name of the plugin task')
    job_name = NonNullColumn(String(256), descr='Name of the job')
    job_uuid = NonNullColumn(UUID(), unique=True,
                             descr='The UUID associated to the job')
    job_starttime = NonNullColumn(TIMESTAMP(),
                                  descr='Start date and time of the job')
    job_endtime = NonNullColumn(TIMESTAMP(),
                                descr='End date and time of the job')
    job_category = NonNullColumn(String(256),
                                 descr='Category of the job.')
    job_descr = NonNullColumn(String(256),
                              descr='Short description of the job')
    job_state = NonNullColumn(job_state_enum,
                               descr='Current state of the job. Possible '
                                     f'values are: {job_state_list}')
    job_status = NonNullColumn(job_status_enum,
                                     descr='Status of the job. '
                                           'Possible values are '
                                           f'{job_status_list}')
    job_task = NonNullColumn(String(256),
                                 descr='Task run for the job.')
    job_status_descr = NonNullColumn(
        String(),
        descr='Short description of the job status',
        comment='Only e.g, \'Job has encountered an exception\''
    )
    job_parent_id = NonNullColumn(
        BIGINT(),
        ForeignKey('poppy.job_log.id_job_log'),
        nullable=True,
        descr='Only mandatory if there is a parent job'
    )

    __tablename__ = 'job_log'
    __table_args__ = {'schema': 'poppy'}

    parent = relationship(
        'JobLog',
        remote_side='JobLog.id_job_log'
    )

    def __repr__(self):
        return (
                'JobLog(' +
                'name={0}'.format(self.job_name) +
                'uuid={0}'.format(self.job_uuid) +
                'state={0}'.format(self.job_state) +
                'status={0}'.format(self.job_status) +
                'start={0}'.format(self.job_starttime) +
                ')'
        )


exception_type_list = ['OK', 'WARNING', 'ERROR']
exception_type_enum = ENUM(*exception_type_list,
                           name='exception_type_type',
                           schema='poppy')

exception_level_list = ['Low', 'Normal', 'High', 'Critical']
exception_level_enum = ENUM(*exception_level_list,
                            name='exception_level_type',
                            schema='poppy')


class JobException(Base):
    """
    The "job_exception" table provides a history of the job exceptions that
    occured in the pipeline.
    """

    id_job_exception = NonNullColumn(BIGINT(), primary_key=True)
    job_log_id = NonNullColumn(
        BIGINT(),
        ForeignKey('poppy.job_log.id_job_log'))
    exception_type = NonNullColumn(exception_type_enum,
                                   descr='Type of the exception. Possible '
                                         f'values are: {exception_type_list}')
    exception_level = NonNullColumn(exception_level_enum,
                                    descr='Level of the exception. Possible'
                                          ' values are: '
                                          f'{exception_level_list}')
    exception_msg = NonNullColumn(String(),
                                  descr='Message related to the exception')

    __tablename__ = 'job_exception'
    __table_args__ = {'schema': 'poppy'}

    job = relationship('JobLog')
