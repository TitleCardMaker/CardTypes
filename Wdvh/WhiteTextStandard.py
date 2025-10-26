from pathlib import Path
from typing import Any

from pydantic import FilePath

from app.cards.base import (
    BaseCardType,
    CardTypeDescription,
    DefaultCardConfig,
    ImageMagickCommands,
)
from app.cards.loader import RemoteFile
from app.schemas.base import BaseCardTypeCustomFontAllText


class WhiteTextStandard(BaseCardType):
    """WDVH's WhiteTextStandard card type."""

    API_DETAILS =  CardTypeDescription(
        name='White Text Standard',
        identifier='Wdvh/WhiteTextStandard',
        example=(
            'https://user-images.githubusercontent.com/17693271/'
            '169709359-ffc9e109-b327-44e9-b78a-7276f77fe917.jpg'
        ),
        creators=['Wdvh', 'CollinHeist'],
        source='remote',
        supports_custom_fonts=True,
        supports_custom_seasons=False,
        supported_extras=[],
        description=[
            'Modification of the Standard Card Type.', 'This Card uses a '
            'different font, smaller text size, and the episode title is '
            'positioned lower than the Standard Card Type.',
        ]
    )

    class CardModel(BaseCardTypeCustomFontAllText):
        font_color: str = '#FFFFFF'
        font_file: FilePath
        separator: str = '•'

    CardConfig = DefaultCardConfig(
        font_file=RemoteFile('Wdvh', 'TerminalDosis-Bold.ttf').resolve(),
        font_color='#FFFFFF',
        title_max_line_width=32,
        title_max_line_count=3,
        title_split_style='top',
    )

    """Source path for the gradient image overlayed over all title cards"""
    __GRADIENT_IMAGE = BaseCardType.BASE_REF_DIRECTORY / 'GRADIENT.png'

    """Default fonts and color for series count text"""
    SEASON_COUNT_FONT = BaseCardType.BASE_REF_DIRECTORY / 'Sequel-Neue.otf'
    EPISODE_COUNT_FONT = BaseCardType.BASE_REF_DIRECTORY / 'Sequel-Neue.otf'
    SERIES_COUNT_TEXT_COLOR = '#FFFFFF'

    __slots__ = (
        'source_file',
        'output_file',
        'title_text',
        'season_text',
        'episode_text',
        'hide_season_text',
        'hide_episode_text',
        'font_color',
        'font_file',
        'font_interline_spacing',
        'font_kerning',
        'font_size',
        'font_stroke_width',
        'font_vertical_shift',
        'separator',
    )


    def __init__(self, *,
            source_file: Path,
            card_file: Path,
            title_text: str,
            season_text: str,
            episode_text: str,
            hide_season_text: bool,
            hide_episode_text: bool,
            font_color: str = CardConfig.font_color,
            font_file: str = str(CardConfig.font_file),
            font_interline_spacing: int = 0,
            font_kerning: float = 1.0,
            font_size: float = 1.0,
            font_stroke_width: float = 1.0,
            font_vertical_shift: int = 0,
            blur: bool = False,
            grayscale: bool = False,
            separator: str = '•',
            **unused: Any,
        ) -> None:
        """Initialize this CardType object."""

        super().__init__(blur, grayscale)

        self.source_file = source_file
        self.output_file = card_file

        # Ensure characters that need to be escaped are
        self.title_text = self.image_magick.escape_chars(title_text)
        self.season_text = self.image_magick.escape_chars(season_text)
        self.episode_text = self.image_magick.escape_chars(episode_text)
        self.hide_season_text = hide_season_text
        self.hide_episode_text = hide_episode_text

        self.font_color = font_color
        self.font_file = font_file
        self.font_interline_spacing = font_interline_spacing
        self.font_kerning = font_kerning
        self.font_size = font_size
        self.font_stroke_width = font_stroke_width
        self.font_vertical_shift = font_vertical_shift

        self.separator = separator


    @property
    def title_text_commands(self) -> ImageMagickCommands:
        """ImageMagick commands to add title text."""

        font_size = 180 * self.font_size
        interline_spacing = -70 + self.font_interline_spacing
        kerning = -1.25 * self.font_kerning
        stroke_width = 4.0 * self.font_stroke_width
        vertical_shift = 145 + self.font_vertical_shift

        return [
            # Global effects
            f'-font "{self.font_file}"',
            f'-kerning {kerning}',
            f'-interword-spacing 50',
            f'-interline-spacing {interline_spacing}',
            f'-pointsize {font_size}',
            f'-gravity south',
            # Black stroke
            f'-fill white',
            f'-stroke "#062A40"',
            f'-strokewidth {stroke_width}',
            f'-annotate +0+{vertical_shift} "{self.title_text}"',
            # Normal text
            f'-fill "{self.font_color}"',
            f'-annotate +0+{vertical_shift} "{self.title_text}"',
        ]


    @property
    def index_text_commands(self) -> ImageMagickCommands:
        """
        Get the ImageMagick commands required to add the index (season
        and episode) text to the image.
        """

        # All text is hidden, return empty commands
        if self.hide_season_text and self.hide_episode_text:
            return []

        # Determine which text to add
        if self.hide_season_text:
            index_text = self.episode_text
        elif self.hide_episode_text:
            index_text = self.season_text
        else:
            index_text = (
                f'{self.season_text} {self.separator} {self.episode_text}'
            )

        return [
            f'-interword-spacing 10',
            f'-kerning 5.42',
            f'-pointsize 85',
            f'-font "{self.EPISODE_COUNT_FONT.resolve()}"',
            f'-gravity center',
            f'-fill white',
            f'-stroke "#062A40"',
            f'-strokewidth 2',
            f'-annotate +0+800 "{index_text}"',
            f'-fill white',
            f'-stroke "#062A40"',
            f'-strokewidth 2',
            f'-annotate +0+800 "{index_text}"',
        ]


    def create(self) -> None:
        """
        Make the necessary ImageMagick and system calls to create this
        object's defined title card.
        """

        self.image_magick.run([
            f'convert',
            # Resize and style source image
            f'"{self.source_file.resolve()}"',
            *self.resize_and_style,
            # Overlay gradient
            f'"{self.__GRADIENT_IMAGE.resolve()}"',
            f'-composite',
            # Add title text
            *self.title_text_commands,
            # Add index text
            *self.index_text_commands,
            # Create and resize output
            *self.resize_output,
            f'"{self.output_file.resolve()}"',
        ])
