"""Implementation of the Clip class, for pointing at media."""

from .. import (
    core,
    media_reference as mr,
    exceptions,
    opentime,
)


@core.register_type
class Clip(core.Item):
    """The base editable object in OTIO.

    Contains a media reference and a trim on that media reference.
    """

    _serializeable_label = "Clip.1"

    def __init__(
        self,
        name=None,
        media_reference=None,
        source_range=None,
    ):
        core.Item.__init__(
            self,
            name=name,
            source_range=source_range,
        )
        # init everything as None first, so that we will catch uninitialized
        # values via exceptions
        self.name = name

        if not media_reference:
            media_reference = mr.MissingReference()
        self.media_reference = media_reference

        self.properties = {}

    name = core.serializeable_field("name", doc="Name of this clip.")
    transform = core.deprecated_field()
    media_reference = core.serializeable_field(
        "media_reference",
        mr.MediaReference,
        "Media reference to the media this clip represents."
    )

    def computed_duration(self):
        """Compute the duration of this clip."""

        if self.source_range is not None:
            return self.source_range.duration

        if self.media_reference.available_range is not None:
            return self.media_reference.available_range.duration

        raise exceptions.CannotComputeDurationError(
            "No source_range on clip or available_range on media_reference for"
            " clip: {}".format(self)
        )

    def trimmed_range(self):
        """Trimmed range of this clip, if set."""
        if self.source_range:
            return self.source_range

        if self.media_reference.available_range is not None:
            return self.media_reference.available_range

        dur = self.duration()
        return opentime.TimeRange(opentime.RationalTime(0, dur.rate), dur)

    def __str__(self):
        return 'Clip("{}", {}, {})'.format(
            self.name,
            self.media_reference,
            self.source_range
        )

    def __repr__(self):
        return (
            'otio.schema.Clip('
            'name={}, '
            'media_reference={}, '
            'source_range={}'
            ')'.format(
                repr(self.name),
                repr(self.media_reference),
                repr(self.source_range),
            )
        )

    def each_clip(self, search_range=None):
        """Yields self."""

        yield self
