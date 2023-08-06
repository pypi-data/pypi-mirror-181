#!/usr/bin/env python
# -*- coding: utf-8 -*-

from poppy.core.pipeline import Pipeline, PipelineError, EmptyLoopError as CoreEmptyLoopError
from poppy.pop.loop import Loop
from poppy.core.logger import logger

__all__ = ["Pop"]


# ensure backward compatibility
class Pop(Pipeline):
    def __init__(self, *args, **kwargs):
        logger.warning("Deprecation Warning: the 'Pop' class was renamed 'Pipeline' and moved in 'poppy.core.pipeline'")
        super().__init__(*args, **kwargs)

    def loop(self, start, end, generator):
        """
        Create a loop between two task in the pipeline topology, according to
        the values given by the provided generator.

        Starts by checking if the topology of the pipeline is existing. Then
        regenerate the topology by security. An instance of the loop is created
        that will override the descendants and ancestors of the start and end
        tasks provided in argument, at the appropriate times.
        """
        # the generation of a loop requires a topology for the pipeline, i.e.
        # that the dependency graph has been created, so checks the basics for
        # its generation
        entry_point = self.start

        # check that the pipeline can be run
        if entry_point is None:
            logger.error(
                "The pipeline doesn't have a topology created and cannot " +
                "generate a loop between tasks {0} and {1}".format(
                    start,
                    end,
                )
            )
            return

        # generate the new topology if necessary
        self.generate_topology(entry_point)

        # create the loop
        loop = Loop(self, start, end, generator)

        # add the loop into the container
        self._loops.append(loop)


class PopError(PipelineError):
    def __init__(self, *args, **kwargs):
        logger.warning("Deprecation Warning: the 'PopError' class was renamed 'PipelineError' and moved in 'poppy.core.pipeline'")
        super().__init__(*args, **kwargs)


class EmptyLoopError(CoreEmptyLoopError):
    def __init__(self, *args, **kwargs):
        logger.warning("Deprecation Warning: the 'EmptyLoopError' class was moved in 'poppy.core.pipeline'")
        super().__init__(*args, **kwargs)
