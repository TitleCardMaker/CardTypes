from pathlib import Path
from typing import Annotated

from pydantic import Field, FilePath, StringConstraints, root_validator

from app.cards.base import (
    BaseCardType,
    CardTypeDescription,
    DefaultCardConfig,
    Extra,
    ImageMagickCommands,
)
from app.cards.loader import RemoteFile
from app.schemas.base import BaseCardTypeCustomFontNoText


class SciFiTitleCard(BaseCardType):
    """
    This class describes a type of BaseCardType that produces title
    cards in a SciFi style as if viewed through a HUD.
    """

    API_DETAILS = CardTypeDescription(
        name='SciFi',
        identifier='azuravian/SciFiTitleCard',
        example=(
            'https://raw.githubusercontent.com/azuravian/myimages/main/'
            'SciFiTitleCard/Example1.jpg'
        ),
        creators=['Azuravian'],
        source='remote',
        supports_custom_fonts=True,
        supports_custom_seasons=False,
        supported_extras=[
            Extra(
                name='Trailing Underscore',
                identifier='add_trailing_underscore',
                description="Whether to add a trailing underscore (_) to the title text",
                tooltip="Either <v>True</v> or <v>False</v>. Default is <v>True</v>."
            ),
            Extra(
                name="Overlay Bottom Color",
                identifier="overlay_bottom_color",
                description="The color of the overlay's bottom layer",
                tooltip="Defaults to <v>rgb(58, 255, 255)</v> (neon blue)."
            ),
            Extra(
                name="Overlay Top Color",
                identifier="overlay_top_color",
                description="The color of overlay's top layer",
                tooltip="Defaults to <v>rgb(255, 49, 255)</v> (hot pink)."
            ),
            Extra(
                name="Overlay Middle Color",
                identifier="overlay_middle_color",
                description="The color of the overlay's middle layer",
                tooltip="Defaults to <v>rgb(255, 255, 255)</v> (white)."
            ),
            Extra(
                name="Overlay Rectangle Color",
                identifier="overlay_rectangles_color",
                description="The color of the overlay rectangles",
                tooltip="Defaults to <v>rgb(102, 211, 122)</v> (neon green)."
            ),
            Extra(
                name="Overlay Base Alpha",
                identifier="overlay_base_alpha",
                description="The transparency of the black surrounding layer",
                tooltip="Value between <v>0.0</v> and <v>1.0</v>. Defaults to <v>1.0</v>."
            ),
            Extra(
                name="Overlay Bottom Alpha",
                identifier="overlay_bottom_alpha",
                description="The transparency of the bottom layer",
                tooltip="Value between <v>0.0</v> and <v>1.0</v>. Defaults to <v>0.6</v>."
            ),
            Extra(
                name="Overlay Top Alpha",
                identifier="overlay_top_alpha",
                description="The transparency of the top layer",
                tooltip="Value between <v>0.0</v> and <v>1.0</v>. Defaults to <v>0.6</v>."
            ),
            Extra(
                name="Overlay Middle Alpha",
                identifier="overlay_middle_alpha",
                description="The transparency of the middle layer",
                tooltip="Value between <v>0.0</v> and <v>1.0</v>. Defaults to <v>0.6</v>."
            ),
            Extra(
                name="Overlay Rectangles Alpha",
                identifier="overlay_rectangles_alpha",
                description="The transparency of the overlay rectangles",
                tooltip="Value between <v>0.0</v> and <v>1.0</v>. Defaults to <v>0.6</v>."
            ),
            Extra(
                name="Episode Text Color",
                identifier="episode_text_color",
                description="The color of the episode text"
            ),
            Extra(
                name="Text Stroke Color",
                identifier="stroke_color",
                description="The color of the text stroke"
            )
        ],
        description=[
            'A multi-overlay card designed to look like a heads up display.',
            'Intended for use in Science Fiction series.',
        ]
    )

    class CardModel(BaseCardTypeCustomFontNoText):
        title_text: str
        episode_text: Annotated[str, StringConstraints(to_upper=True)]
        hide_episode_text: bool = False
        font_color: str = 'white'
        font_file: FilePath
        add_trailing_underscore: bool = True
        overlay_bottom_color: str = 'rgb(58, 255, 255)'
        overlay_middle_color: str = 'rgb(255, 255, 255)'
        overlay_top_color: str = 'rgb(255, 49, 255)'
        overlay_rectangles_color: str = 'rgb(102, 211, 122)'
        overlay_base_alpha: Annotated[float, Field(ge=0.0, le=1.0)] = 1.0
        overlay_bottom_alpha: Annotated[float, Field(ge=0.0, le=1.0)] = 0.6
        overlay_middle_alpha: Annotated[float, Field(ge=0.0, le=1.0)] = 0.6
        overlay_top_alpha: Annotated[float, Field(ge=0.0, le=1.0)] = 0.6
        overlay_rectangles_alpha: Annotated[float, Field(ge=0.0, le=1.0)] = 0.6
        episode_text_color: str = 'white'
        stroke_color: str = 'black'

        @root_validator(skip_on_failure=True, allow_reuse=True)
        def toggle_text_hiding(cls, values):
            values['hide_episode_text'] |= (len(values['episode_text']) == 0)

            return values

    """Default configuration for this card type"""
    TITLE_FONT = RemoteFile('azuravian', 'ref/SciFi/PcapTerminal-BO9B.ttf').resolve()
    CardConfig = DefaultCardConfig(
        font_file=TITLE_FONT,
        font_color='white',
        title_max_line_width=20,
        title_max_line_count=3,
        title_split_style='bottom',
        episode_text_format='S{season_number:02}E{episode_number:02}',
    )

    STROKE_COLOR = 'black'

    """Characteristics of the episode text"""
    EPISODE_TEXT_FONT = str(RemoteFile('azuravian', 'ref/SciFi/PcapTerminal-BO9B.ttf'))

    """Path to the hud images to overlay on all source images"""
    __OVERLAY_BASE = str(RemoteFile('azuravian', 'ref/SciFi/Base.png'))
    __OVERLAY_BOTTOM = str(RemoteFile('azuravian', 'ref/SciFi/Bottom.png'))
    __OVERLAY_MIDDLE = str(RemoteFile('azuravian', 'ref/SciFi/Middle.png'))
    __OVERLAY_TOP = str(RemoteFile('azuravian', 'ref/SciFi/Top.png'))
    __OVERLAY_RECTANGLES = str(RemoteFile('azuravian', 'ref/SciFi/Rectangles.png'))

    __slots__ = (
        'source_file', 'output_file', 'title_text', 'episode_text',
        'hide_episode_text', 'font_color', 'stroke_color', 'font_file',
        'font_interline_spacing', 'font_interword_spacing', 'font_kerning',
        'font_size', 'font_stroke_width', 'font_vertical_shift',
        'add_trailing_underscore', 'overlay_bottom_color',
        'overlay_middle_color', 'overlay_top_color', 'overlay_rectangles_color',
        'overlay_base_alpha', 'overlay_middle_alpha', 'overlay_bottom_alpha',
        'overlay_top_alpha', 'overlay_rectangles_alpha', 'episode_text_color',
    )

    def __init__(self, *,
            source_file: Path,
            card_file: Path,
            title_text: str,
            episode_text: str,
            hide_episode_text: bool = False,
            font_color: str = CardConfig.font_color,
            font_file: str = str(CardConfig.font_file),
            font_interline_spacing: int = 0,
            font_interword_spacing: int = 0,
            font_kerning: float = 1.0,
            font_size: float = 1.0,
            font_stroke_width: float = 1.0,
            font_vertical_shift: int = 0,
            blur: bool = False,
            grayscale: bool = False,
            add_trailing_underscore: bool = True,
            overlay_bottom_color: str = 'rgb(58, 255, 255)',
            overlay_middle_color: str = 'rgb(255, 255, 255)',
            overlay_top_color: str = 'rgb(255, 49, 255)',
            overlay_rectangles_color: str = 'rgb(102, 211, 122)',
            overlay_base_alpha: float = 1.0,
            overlay_bottom_alpha: float = 0.6,
            overlay_middle_alpha: float = 0.6,
            overlay_top_alpha: float = 0.6,
            overlay_rectangles_alpha: float = 0.6,
            episode_text_color: str = CardConfig.font_color,
            stroke_color: str = STROKE_COLOR,
            **unused,
        ) -> None:
        """Initialize the CardType object."""

        # Initialize the parent class - this sets up an ImageMagickInterface
        super().__init__(blur, grayscale)

        # Store source and output file
        self.source_file = source_file
        self.output_file = card_file

        # Ensure characters that need to be escaped are
        self.title_text = self.image_magick.escape_chars(title_text)
        self.episode_text = self.image_magick.escape_chars(episode_text)
        self.hide_episode_text = hide_episode_text

        # Font customizations
        self.font_color = font_color
        self.font_file = font_file
        self.font_interline_spacing = font_interline_spacing
        self.font_interword_spacing = font_interword_spacing
        self.font_kerning = font_kerning
        self.font_size = font_size
        self.font_stroke_width = font_stroke_width
        self.font_vertical_shift = font_vertical_shift

        # Optional extras
        self.add_trailing_underscore = add_trailing_underscore
        self.episode_text_color = episode_text_color
        self.overlay_bottom_color = overlay_bottom_color
        self.overlay_top_color = overlay_top_color
        self.overlay_middle_color = overlay_middle_color
        self.overlay_rectangles_color = overlay_rectangles_color
        self.overlay_base_alpha = 1 / overlay_base_alpha
        self.overlay_bottom_alpha = 1 / overlay_bottom_alpha
        self.overlay_top_alpha = 1 / overlay_top_alpha
        self.overlay_middle_alpha = 1 / overlay_middle_alpha
        self.overlay_rectangles_alpha = 1 / overlay_rectangles_alpha
        self.stroke_color = stroke_color


    @property
    def title_text_command(self) -> ImageMagickCommands:
        """
        ImageMagick commands to implement the title text's global
        effects. Specifically the the font, kerning, fontsize, and
        center gravity.
        """

        title_text = (
            self.title_text + ('_' if self.add_trailing_underscore else '')
        )

        font_size = 157.41 * self.font_size
        interline_spacing = -22 + self.font_interline_spacing
        interword_spacing = 50 + self.font_interword_spacing
        kerning = -1.25 * self.font_kerning
        stroke_width = 3.0 * self.font_stroke_width
        vertical_shift = 215 + self.font_vertical_shift

        return [
            f'-font "{self.font_file}"',
            f'-kerning {kerning}',
            f'-interword-spacing {interword_spacing}',
            f'-interline-spacing {interline_spacing}',
            f'-pointsize {font_size}',
            f'-gravity southeast',
            f'-strokewidth {stroke_width}',
            f'-stroke {self.stroke_color}',
            f'-fill {self.font_color}',
            f'-annotate +200+{vertical_shift} "{title_text}"'
        ]


    @property
    def index_text_command(self) -> ImageMagickCommands:
        """
        Get the ImageMagick commands required to add the index (season
        and episode) text to the image.
        """

        # All text is hidden, return 
        if self.hide_episode_text:
            return []
   
        return [
            f'-font "{self.EPISODE_TEXT_FONT}"',
            f'-fill "{self.episode_text_color}"',
            f'-kerning 5.42',
            f'-pointsize 67.75',
            f'-gravity northwest',
            f'-strokewidth 3',
            f'-stroke black',
            f'+interword-spacing',
            f'-annotate +150+100 "{self.episode_text}"'
        ]


    def overlay_hud(self,
            overlay: str,
            color: str,
            alpha: float,
        ) -> ImageMagickCommands:
        """
        Edit the rectangles hud layer to selected color and transparency.
        
        Args:
            overlay: Filepath (as a string) to the overlay file.
            color: Color to colorize the overlay with.
            alpha: Transparency of this overlay.

        Returns:
            List of ImageMagick commands.
        """

        return [
            fr'\(',
                f'"{overlay}"',
                f'-fill "{color}"',
                f'-colorize 100%',
                f'-alpha set',
                f'-channel A',
                f'-evaluate Divide {alpha}',
            fr'\)',
            f'-composite'
        ]


    def create(self) -> None:
        """Create the title card as defined by this object."""

        self.image_magick.run([
            f'convert "{self.source_file.resolve()}"',
            # Resize and apply styles
            *self.resize_and_style,
            # Overlay huds
            *self.overlay_hud(self.__OVERLAY_BASE, 'black', self.overlay_base_alpha),
            *self.overlay_hud(self.__OVERLAY_BOTTOM, self.overlay_bottom_color, self.overlay_bottom_alpha),
            *self.overlay_hud(self.__OVERLAY_MIDDLE, self.overlay_middle_color, self.overlay_middle_alpha),
            *self.overlay_hud(self.__OVERLAY_TOP, self.overlay_top_color, self.overlay_top_alpha),
            *self.overlay_hud(self.__OVERLAY_RECTANGLES, self.overlay_rectangles_color, self.overlay_rectangles_alpha),
            # Put title text
            *self.title_text_command,
            # Put season/episode text
            *self.index_text_command,
            # Attempt to overlay mask
            *self.add_overlay_mask(self.source_file),
            # Create and resize output
            *self.resize_output,
            f'"{self.output_file.resolve()}"',
        ])
