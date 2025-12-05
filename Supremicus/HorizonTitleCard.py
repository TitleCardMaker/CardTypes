from pathlib import Path
from typing import Annotated, ClassVar, Literal, Self

from pydantic import Field, FilePath, field_validator, model_validator

from app.cards.base import (
    BaseCardType,
    CardTypeDescription,
    DefaultCardConfig,
    Extra,
    ImageMagickCommands,
)
from app.cards.loader import RemoteDirectory
from app.info.episode import EpisodeInfo
from app.schemas.base import (
    BaseCardModel,
    BaseCardTypeCustomFontAllText,
    FontSize,
)


class HorizonTitleCard(BaseCardType):
    """
    CardType that produces title cards similar to the left or right
    aligned with vertically centered text with optional symbol similar
    to the custom cards found on MediUX. CRT TV overlay (nobezel or
    bezel) with optional watched style based on Yozora's Retro title
    card for shows like Stranger Things with a retro theme.
    """

    """API Parameters"""
    API_DETAILS = CardTypeDescription(
        name='Horizon',
        identifier='Supremicus/HorizonTitleCard',
        example=(
            'https://raw.githubusercontent.com/TitleCardMaker/'
            'CardTypes/web-ui-develop/Supremicus/'
            'HorizonTitleCard.preview.jpg'
        ),
        creators=['Supremicus'],
        source='remote',
        supports_custom_fonts=True,
        supports_custom_seasons=True,
        supported_extras=[
            Extra(
                name='Stroke Text Color',
                identifier='stroke_color',
                description='Color to use for the text stroke',
                tooltip='Default is <c>black</c>.',
                default='black'
            ),
            Extra(
                name='Episode Text Vertical Shift',
                identifier='episode_text_vertical_shift',
                description='Vertical shift for episode text',
                tooltip=(
                    'Additional vertical shift to apply to the season and '
                    'episode text. Unit is pixels.'
                ),
                default=0,
            ),
            Extra(
                name='Episode Text Font',
                identifier='episode_text_font',
                description='Font to use for the season and episode text',
                tooltip=(
                    'This can be just a file name if the font file is in the '
                    'Series source directory, <v>{font_file}</v> to match '
                    'the Font used for the title text, or a full path to the '
                    'font file.'
                ),
            ),
            Extra(
                name='Episode Text Font Size',
                identifier='episode_text_font_size',
                description='Size adjustment for the season and episode text',
                tooltip='Number ≥<v>0.0</v>. Default is <v>1.0</v>.',
                default=1.0,
            ),
            Extra(
                name='Episode Text Color',
                identifier='episode_text_color',
                description='Color to use for the episode text',
                tooltip='Defaults to match the Title Color.',
            ),
            Extra(
                name='Episode Stroke Text Color',
                identifier='episode_text_stroke_color',
                description='Color to use for the stroke of the episode text',
                tooltip='Defaults to match the Stroke Text Color.',
            ),
            Extra(
                name='Episode Text Kerning',
                identifier='episode_text_kerning',
                description='Spacing between characters for the episode text',
                tooltip='Default is <v>0</v>. Unit is pixels.',
                default=0,
            ),
            Extra(
                name='Episode Text Interword Spacing',
                identifier='episode_text_interword_spacing',
                description='Spacing between words for the episode text',
                tooltip='Default is <v>0</v>. Unit is pixels.',
                default=0,
            ),
            Extra(
                name='Separator Character / Image',
                identifier='separator',
                description='Character or image to separate season and episode text',
                tooltip=(
                    'Default is <v>•</v>. You may also provide an image file '
                    'name if the image file is in the Series source directory, '
                    'or a full path to an image file to use as the separator.'
                ),
                default='•',
            ),
            Extra(
                name='Separator Image Padding',
                identifier='separator_image_padding',
                description='Padding to apply to the separator image',
                tooltip=(
                    'Additional padding to apply to the left and right of the '
                    'separator image if used. Default is <v>0</v>. Unit is pixels.'
                ),
                default=0,
            ),
            Extra(
                name='Separator Image Height',
                identifier='separator_image_height',
                description='Adjust the height of the separator image',
                tooltip=(
                    'Adjusts the height of the separator image if used '
                    'keeping aspect ratio. Default is <v>100</v>. Unit is pixels.'
                ),
                default=100,
            ),
            Extra(
                name='Separator Image Y Offset',
                identifier='separator_image_y_offset',
                description='Adjust the vertical position of the separator image',
                tooltip=(
                    'Adjusts the vertical position of the separator image if used. '
                    'Default is <v>0</v>. Unit is pixels.'
                ),
                default=0,
            ),
            Extra(
                name='Separator Image Stroke',
                identifier='separator_image_use_stroke',
                description='Whether to apply a stroke to the separator image',
                tooltip=(
                    'Automatically apply a stroke to the separator image to match '
                    'text stroke width of text. Either <v>True</v> or <v>False</v>. '
                    'Default is <v>True</v>.'
                    '<br><b>WARNING</b>: Artifacting will occur on stray pixels.'
                ),
                default='True',
            ),
            Extra(
                name='Horizontal Alignment',
                identifier='h_align',
                description='Horizontal alignment of text',
                tooltip=(
                    'Either <v>left</v>, <v>center</v>, or <v>right</v>. '
                    'Default is <v>left</v>.'
                ),
                default='left',
            ),
            Extra(
                name='Symbol',
                identifier='symbol',
                description='Add a custom symbol behind the text',
                tooltip=(
                    'Either <v>acolyte</v>, <v>ahsoka</v>, <v>andor</v>, '
                    '<v>bobafett<v>, <v>mandalorian</v>, <v>obiwan</v>, or '
                    '<v>witcher</v> to use a built-in symbol; or <v>logo</v> '
                    'to use the Series logo.'
                ),
            ),
            Extra(
                name='Symbol Opacity',
                identifier='symbol_opacity',
                description='Adjust opacity of the symbol',
                tooltip=(
                    'Number between <v>0</v> and <v>100</v>. <v>0</v>% being '
                    'fully transparent, <v>100</v>% being fully opaque. Unit '
                    'is percent.'
                ),
                default=100,
            ),
            Extra(
                name='CRT TV Overlay',
                identifier='crt_overlay',
                description='CRT TV Overlay Toggle',
                tooltip=(
                    'Whether to display the CRT TV overlay. Either '
                    '<v>nobezel</v>, or <v>bezel</v>. Default is no overlay.'
                ),
            ),
            Extra(
                name='CRT TV Watched/Unwatched Overlay',
                identifier='crt_state_overlay',
                description='CRT TV Overlay Watched-Status Toggle',
                tooltip=(
                    'Whether to change the CRT overlay with the watched status '
                    'of the Episode. Either <v>True</v> or <v>False</v>. '
                    'Default is <v>False</v>. Will only work if the CRT TV '
                    'Overlay Toggle is enabled.'
                ),
                default='False',
            ),
            Extra(
                name='Gradient Omission',
                identifier='omit_gradient',
                description='Whether to omit the gradient overlay',
                tooltip=(
                    'Either <v>True</v> or <v>False</v>. Set to <v>False</v> '
                    'if you have trouble reading the text on brighter images.'
                    'Default is <v>True</v>.'
                ),
                default='True',
            ),
        ],
        description=[
            'Produce TitleCards with left or right aligned centered text with '
            'an optional symbol similar to those found on MediUX. CRT TV '
            'overlay for shows like Stranger Things with a retro theme.'
        ],
    )

    """Remote file directories"""
    FONT_DIRECTORY: ClassVar[RemoteDirectory] = RemoteDirectory('Supremicus', 'ref/fonts')
    SYMBOL_DIRECTORY: ClassVar[RemoteDirectory] = RemoteDirectory('Supremicus', 'ref/symbols')
    OVERLAY_DIRECTORY: ClassVar[RemoteDirectory] = RemoteDirectory('Supremicus', 'ref/overlays')

    """Default configuration for this card type"""
    CardConfig = DefaultCardConfig(
        font_file=(FONT_DIRECTORY / 'HelveticaNeue-Bold.ttf').resolve(),
        font_color='white',
        font_case='upper',
        font_replacements={},
        title_max_line_width=16,
        title_max_line_count=4,
        title_split_style='top',
        episode_text_format='EPISODE {episode_number}',
    )

    """Characteristics of episode text"""
    EPISODE_TEXT_FONT = FONT_DIRECTORY / 'ExoSoft-Medium.ttf'

    """Source path for symbol images to be overlayed behind text"""
    __SYMBOL_IMAGE_ACOLYTE = SYMBOL_DIRECTORY / 'acolyte.png'
    __SYMBOL_IMAGE_AHSOKA = SYMBOL_DIRECTORY / 'ahsoka.png'
    __SYMBOL_IMAGE_ANDOR = SYMBOL_DIRECTORY / 'andor.png'
    __SYMBOL_IMAGE_BOBAFETT = SYMBOL_DIRECTORY / 'bobafett.png'
    __SYMBOL_IMAGE_MANDALORIAN = SYMBOL_DIRECTORY / 'mandalorian.png'
    __SYMBOL_IMAGE_OBIWAN = SYMBOL_DIRECTORY / 'obiwan.png'
    __SYMBOL_IMAGE_WITCHER = SYMBOL_DIRECTORY / 'witcher.png'

    """Source path for CRT overlays to be overlayed if enabled"""
    __OVERLAY_PLAIN = OVERLAY_DIRECTORY / 'overlay_plain.png'
    __OVERLAY_PLAIN_BEZEL = OVERLAY_DIRECTORY / 'overlay_plain_bezel.png'
    __OVERLAY_PLAY = OVERLAY_DIRECTORY / 'overlay_play.png'
    __OVERLAY_PLAY_BEZEL = OVERLAY_DIRECTORY / 'overlay_play_bezel.png'
    __OVERLAY_REWIND = OVERLAY_DIRECTORY / 'overlay_rewind.png'
    __OVERLAY_REWIND_BEZEL = OVERLAY_DIRECTORY / 'overlay_rewind_bezel.png'

    """Source path for gradient images"""
    __GRADIENT_IMAGE = OVERLAY_DIRECTORY / 'radial_gradient.png'
    __GRADIENT_IMAGE_CENTERED = OVERLAY_DIRECTORY / 'radial_gradient_centered.png'

    __slots__ = (
        'source_file',
        'output_file',
        'title_text',
        'season_text',
        'episode_text',
        'hide_season_text',
        'hide_episode_text',
        'font_file',
        'font_color',
        'font_size',
        'font_stroke_width',
        'font_interline_spacing',
        'font_interword_spacing',
        'font_kerning',
        'font_vertical_shift',
        'stroke_color',
        'episode_text_vertical_shift',
        'episode_text_font',
        'episode_text_font_size',
        'episode_text_color',
        'episode_text_stroke_color',
        'episode_text_kerning',
        'episode_text_interword_spacing',
        'separator',
        'separator_image_padding',
        'separator_image_height',
        'separator_image_y_offset',
        'separator_image_use_stroke',
        'h_align',
        'symbol',
        'symbol_opacity',       
        'logo',
        'crt_overlay',
        'crt_state_overlay',
        'omit_gradient',
        'watched',
    )

    def __init__(self, *,
            source_file: Path,
            card_file: Path,
            title_text: str,
            season_text: str,
            episode_text: str,
            hide_season_text: bool = False,
            hide_episode_text: bool = False,
            font_file: str = str(CardConfig.font_file),
            font_color: str = CardConfig.font_color,
            font_size: float = 1.0,
            font_stroke_width: float = 1.0,
            font_interline_spacing: int = 0,
            font_interword_spacing: int = 0,
            font_kerning: float = 1.0,
            font_vertical_shift: int = 0,
            blur: bool = False,
            grayscale: bool = False,
            stroke_color: str = 'black',
            episode_text_vertical_shift: int = 0,
            episode_text_font: Path = EPISODE_TEXT_FONT.resolve(),
            episode_text_font_size: float = 1.0,
            episode_text_color: str | None = None,
            episode_text_stroke_color: str | None = None,
            episode_text_kerning: int = 0,
            episode_text_interword_spacing: int = 0,
            separator: str = '•',
            separator_image_padding: int = 0,
            separator_image_height: int = 100,
            separator_image_y_offset: int = 0,
            separator_image_use_stroke: bool = True,
            h_align: Literal['left', 'center', 'right'] = 'left',
            symbol: None | Literal[
                'acolyte',
                'ashoka',
                'andor',
                'bobafett',
                'mandalorian',
                'obiwan',
                'witcher',
                'logo',
            ] = None,
            symbol_opacity: int = 100,
            logo_file: Path | None = None,
            crt_overlay: Literal['nobezel', 'bezel'] | None = None,
            crt_state_overlay: bool = False,
            omit_gradient: bool = True,
            watched: bool = True,
            **unused,
        ) -> None:
        """Construct a new instance of this card."""

        # Initialize the parent class - this sets up an ImageMagickInterface
        super().__init__(blur, grayscale)

        self.source_file = source_file
        self.output_file = card_file

        # Ensure characters that need to be escaped are
        self.title_text = self.image_magick.escape_chars(title_text)
        self.season_text = self.image_magick.escape_chars(season_text)
        self.episode_text = self.image_magick.escape_chars(episode_text)
        self.hide_season_text = hide_season_text
        self.hide_episode_text = hide_episode_text

        # Font customizations
        self.font_file = font_file
        self.font_color = font_color
        self.font_size = 140 * font_size
        self.font_stroke_width = font_stroke_width
        self.font_interline_spacing = font_interline_spacing
        self.font_interword_spacing = font_interword_spacing
        self.font_kerning = 1.0 * font_kerning
        self.font_vertical_shift = font_vertical_shift

        # Optional extras
        self.stroke_color = stroke_color
        self.episode_text_vertical_shift = episode_text_vertical_shift
        self.episode_text_font = episode_text_font
        self.episode_text_font_size = 60 * episode_text_font_size
        self.episode_text_color = episode_text_color
        self.episode_text_stroke_color = episode_text_stroke_color
        self.episode_text_kerning = episode_text_kerning
        self.episode_text_interword_spacing = episode_text_interword_spacing
        self.separator = separator
        self.separator_image_padding = separator_image_padding
        self.separator_image_height = separator_image_height
        self.separator_image_y_offset = separator_image_y_offset
        self.separator_image_use_stroke = separator_image_use_stroke
        self.h_align = h_align
        self.symbol = symbol
        self.symbol_opacity = symbol_opacity
        self.logo = logo_file
        self.crt_overlay = crt_overlay
        self.crt_state_overlay = crt_state_overlay
        self.omit_gradient = omit_gradient
        self.watched = watched


    def stroke_separator_image(self, image_path: str | Path) -> ImageMagickCommands:
        """
        Return ImageMagick commands to apply a stroke/outline to an image.
        Resizes separator image to separator image height, applies a border
        and padding to avoid clipping, and then applies stroke.

        Returns the image with a stroke or just the image if no stroke is defined.
        """

        # Return the image path as a command if no stroke is to be applied
        if not self.separator_image_use_stroke \
            or not self.font_stroke_width or self.font_stroke_width == 0:
            return [f'"{image_path}"']

        stroke_color = self.episode_text_stroke_color
        # Divide stoke width by 2 to match imagemagick stroke of half
        # on inside and half on outside of text
        stroke_width = round(4.0 * self.font_stroke_width) / 2
        # Apply border to avoid clipping of stroke + some extra padding
        border_width = stroke_width + 2

        return [
            fr'\(',
                fr'\(',
                    f'"{image_path}"',
                    f'-resize x{self.separator_image_height}',
                    f'-bordercolor none',
                    f'-border {border_width}',
                    f'-write mpr:bordered',
                    f'+delete',
                fr'\)',
                fr'\(',
                    f'mpr:bordered',
                    f'-alpha extract',
                    f'-morphology dilate disk:{stroke_width}',
                fr'\)',
                fr'\(',
                    f'mpr:bordered',
                    f'-alpha extract',
                fr'\)',
                f'-compose minus_src',
                f'-composite',
                f'-threshold 0',
                f'-write mpr:stroke',
                f'+delete',
                fr'\(',
                    f'mpr:bordered',
                    f'-alpha off',
                    f'-fill {stroke_color}',
                    f'-colorize 100',
                    f'mpr:stroke',
                    f'-compose copy_opacity',
                    f'-composite',
                fr'\)',
                f'mpr:bordered',
                f'-compose over',
                f'-composite',
                f'-alpha on',
            fr'\)',
        ]


    @property
    def index_text_commands(self) -> ImageMagickCommands:
        """
        Subcommand for adding the index text and separator to the image.
        Combining it all together with gravity center for alignment and
        composing together, then smushing horizontally into one image
        layer like so:

        Top layer
        +--------+-----------+--------+
        |  text  | separator |  text  |
        +--------+-----------+--------+
        | stroke |  stroke   | stroke |
        +--------+-----------+--------+
        Bottom layer
        """

        # All text hidden, return empty commands
        if self.hide_season_text and self.hide_episode_text:
            return []

        # Set index text based on which text is hidden/not
        if self.hide_season_text:
            index_text = self.episode_text
        elif self.hide_episode_text:
            index_text = self.season_text
        else:
            index_text = f'{self.season_text} {self.separator} {self.episode_text}'

        # Use image separator if applicable and no text is hidden
        if not (self.hide_season_text or self.hide_episode_text) and not \
            (isinstance(self.separator, str) and len(self.separator) == 1):

            return [
                # Season text
                fr'\(',
                    f'-font "{self.episode_text_font}"',
                    f'-pointsize {self.episode_text_font_size}',
                    f'-kerning {self.episode_text_kerning}',
                    f'-interword-spacing {self.episode_text_interword_spacing}',
                    f'-gravity center',
                    fr'\(',
                        *self._index_text_stroke_commands(self.season_text),
                    fr'\)',
                    fr'\(',
                        f'-fill "{self.episode_text_color}"',
                        f'label:"{self.season_text}"',
                    fr'\)',
                    *([f'-compose over'] if self.font_stroke_width != 0 else []),
                    *([f'-composite'] if self.font_stroke_width != 0 else []),
                fr'\)',
                # Separator image (resize height only to keep aspect ratio)
                fr'\(',
                    # Create empty canvas to allow y offset positioning
                    f'xc:none',
                    # Double canvas size to accommodate separator image + offset
                    f'-resize x{self.separator_image_height * 2}',
                    fr'\(',
                        *self.stroke_separator_image(self.separator),
                        f'-resize x{self.separator_image_height}',
                        f'-geometry +0{self.separator_image_y_offset:+}',
                    fr'\)',
                    f'-composite',
                fr'\)',
                # Episode text
                fr'\(',
                    fr'\(',
                        *self._index_text_stroke_commands(self.episode_text),  
                    fr'\)',
                    fr'\(',
                        f'-fill "{self.episode_text_color}"',
                        f'label:"{self.episode_text}"',
                    fr'\)',
                    *([f'-compose over'] if self.font_stroke_width != 0 else []),
                    *([f'-composite'] if self.font_stroke_width != 0 else []),
                fr'\)',
                f'+smush {20 + self.separator_image_padding}',
            ]

        # Return normal text commands if no image separator
        return [
            f'-font "{self.episode_text_font}"',
            f'-pointsize {self.episode_text_font_size}',
            f'-gravity center',
            f'-kerning {self.episode_text_kerning}',
            f'-interword-spacing {self.episode_text_interword_spacing}',
            *self._index_text_stroke_commands(index_text),
            f'-fill "{self.episode_text_color}"',
            f'label:"{index_text}"',
            *([f'-composite'] if self.font_stroke_width != 0 else []),
        ]


    def _index_text_stroke_commands(self, index_text: str) -> ImageMagickCommands:
        """Generate stroke commands for index text."""

        # If no stroke, return empty commands
        if self.font_stroke_width == 0:
            return []

        stroke_width = 4.0 * self.font_stroke_width

        return [
            f'-fill "{self.episode_text_stroke_color}"',
            f'-stroke "{self.episode_text_stroke_color}"',
            f'-strokewidth {stroke_width}',
            f'label:"{index_text}"',
            f'-stroke none',
        ]


    @property
    def title_text_commands(self) -> ImageMagickCommands:
        """
        Subcommand for adding the title text to the image. Combines
        it all together with gravity center for alignment and
        composing into one image layer like so:

        Top layer
        +--------+
        |  text  |
        +--------+
        | stroke |
        +--------+
        Bottom layer
        """

        # If no title text, return empty commands
        if not self.title_text:
            return []

        return [
            f'-font "{self.font_file.resolve()}"',
            f'-pointsize {self.font_size}',
            f'-gravity center',
            f'-kerning {self.font_kerning}',
            f'-interline-spacing {self.font_interline_spacing}',
            f'-interword-spacing {self.font_interword_spacing}',
            *self._title_text_stroke_commands(),
            f'-fill "{self.font_color}"',
            f'label:"{self.title_text}"',
            *([f'-composite'] if self.font_stroke_width != 0 else []),
        ]


    def _title_text_stroke_commands(self) -> ImageMagickCommands:
        """Generate stroke/outline commands for title text."""

        # If no stroke, return empty commands
        if self.font_stroke_width == 0:
            return []

        stroke_width = 4.0 * self.font_stroke_width

        return [
            f'-fill "{self.stroke_color}"',
            f'-stroke "{self.stroke_color}"',
            f'-strokewidth {stroke_width}',
            f'label:"{self.title_text}"',
            f'-stroke none',
        ]


    @property
    def combine_text_commands(self) -> ImageMagickCommands:
        """
        Subcommands to combine index and title text layers together.
        Combines into one image layer, trims and aligns it using gravity
        center. Smush pulled the separator image into whitespace so
        had to resort to title_height and geometry for positioning.
        """

        # Auto adjust y offset to try and keep text horizontally
        # centered when using separator image, some fonts with uneven
        # metrics may be a couple of pixels off
        if not (self.hide_season_text or self.hide_episode_text) and not \
            (isinstance(self.separator, str) and len(self.separator) == 1) and \
            self.separator_image_height > self.episode_text_font_size:
            img_calc = (self.separator_image_height - self.episode_text_font_size) / 2
            auto_adjust_y = (img_calc - self.separator_image_y_offset) / 2
        else:
            auto_adjust_y = 0

        # Get height of title text
        title_text_height_command = [
            f'-font "{self.font_file.resolve()}"',
            f'-pointsize {self.font_size}',
            f'-interline-spacing {self.font_interline_spacing}',
            f'-strokewidth {4.0 * self.font_stroke_width}',
            f'label:"{self.title_text}"',
        ]
        _, title_height = self.image_magick.get_text_label_dimensions(
            title_text_height_command
        )

        x = -700 if self.h_align == 'left' else (700 if self.h_align == 'right' else 0)
        y = 0 + self.font_vertical_shift - auto_adjust_y
        index_y = title_height + 42 + self.episode_text_vertical_shift

        # Build text layers to combine based on what text isn't hidden
        layers = []
        if self.index_text_commands:
            layers += [
                fr'\(',
                    *self.index_text_commands,
                    f'-trim',
                fr'\)',
                f'-gravity south',
                f'-geometry +0{index_y:+}',
                f'-composite',
            ]

        if self.title_text_commands:
            layers += [
                fr'\(',
                    *self.title_text_commands,
                    f'-trim',
                fr'\)',
                f'-gravity south',
                f'-geometry +0+0',
                f'-composite',
            ]

        if layers:
            return [
                fr'\(',
                    f'xc:none',
                    f'-resize {self.WIDTH}x{self.HEIGHT}!',
                    *layers,
                fr'\)',
                f'-trim',
                f'-gravity center',
                f'-geometry {x:+}{y:+}',
                f'-composite',
            ]

        else:
            # Return empty if both text layers are empty
            # Should never reach here but just in case
            return []


    @property
    def add_symbol_image_commands(self) -> ImageMagickCommands:
        """Add the symbol image behind the text, if applicable."""

        SYMBOLS = {
            'acolyte': self.__SYMBOL_IMAGE_ACOLYTE,
            'ahsoka': self.__SYMBOL_IMAGE_AHSOKA,
            'andor': self.__SYMBOL_IMAGE_ANDOR,
            'bobafett': self.__SYMBOL_IMAGE_BOBAFETT,
            'mandalorian': self.__SYMBOL_IMAGE_MANDALORIAN,
            'obiwan': self.__SYMBOL_IMAGE_OBIWAN,
            'witcher': self.__SYMBOL_IMAGE_WITCHER,
            'logo': self.logo,
        }
        symbol_image: Path | None = SYMBOLS.get(self.symbol, None)
        if not symbol_image or not symbol_image.exists():
            return []

        x = -700 if self.h_align == 'left' else (700 if self.h_align == 'right' else 0)

        return [
            f'-gravity center',
            fr'\(',
                f'"{symbol_image.resolve()}"',
                f'-resize x850',
                f'-resize 850x850\>',
                f'-matte',
                f'-channel A',
                f'+level 0,{self.symbol_opacity}%',
                f'+channel',
            fr'\)',
            f'-geometry {x:+}+0',
            f'-composite',
        ]


    @property
    def add_crt_overlay_commands(self) -> ImageMagickCommands:
        """Add the CRT TV overlay to this object's source image."""

        if self.crt_overlay is None:
            return []
        # Select CRT overlay based on watch status
        if self.crt_overlay == 'nobezel':
            if self.crt_state_overlay and not self.watched:
                crt_overlay_image = self.__OVERLAY_PLAY
            elif self.crt_state_overlay and self.watched:
                crt_overlay_image = self.__OVERLAY_REWIND
            else:
                crt_overlay_image = self.__OVERLAY_PLAIN
        elif self.crt_overlay == 'bezel':
            if self.crt_state_overlay and not self.watched:
                crt_overlay_image = self.__OVERLAY_PLAY_BEZEL
            elif self.crt_state_overlay and self.watched:
                crt_overlay_image = self.__OVERLAY_REWIND_BEZEL
            else:
                crt_overlay_image = self.__OVERLAY_PLAIN_BEZEL
        else:
            crt_overlay_image = self.__OVERLAY_PLAIN

        return [
            f'"{crt_overlay_image.resolve()}"',
            f'-composite',
        ]


    @property
    def gradient_commands(self) -> ImageMagickCommands:
        """
        Add the gradient overlay to this object's source image. This rotates
        and repositions the gradient overlay based on the text position.
        """

        if self.omit_gradient:
            return []

        if self.h_align in ('left', 'right'):
            rotation = 0 if self.h_align == 'left' else 180
            gradient_image = self.__GRADIENT_IMAGE
        else:
            rotation = 0
            gradient_image = self.__GRADIENT_IMAGE_CENTERED

        return [
            fr'\(',
                f'"{gradient_image.resolve()}"',
                f'-rotate {rotation}',
            fr'\)',
            f'-composite',
        ]


    @staticmethod
    def SEASON_TEXT_FORMATTER(episode_info: EpisodeInfo) -> str:
        """
        Fallback season title formatter.

        Args:
            episode_info: Info of the Episode whose season text is being
                determined.

        Returns:
            'SPECIALS' if the season number is 0.
            'SEASON {x}' for the given season number.
        """

        if episode_info.season_number == 0:
            return 'SPECIALS'

        return f'SEASON {episode_info.season_number}'


    def create(self) -> None:
        """Create this object's defined Title Card."""

        self.image_magick.run([
            f'convert',
            f'"{self.source_file.resolve()}"',
            # Resize and optionally blur source image
            *self.resize_and_style,
            # Overlay gradient
            *self.gradient_commands,
            # Apply symbol image behind text
            *self.add_symbol_image_commands,
            # Add combined index and title text
            *self.combine_text_commands,
            # Add CRT TV overlay
            *self.add_crt_overlay_commands,
            # Attempt to overlay mask
            *self.add_overlay_mask(self.source_file),
            # Create card
            *self.resize_output,
            f'"{self.output_file.resolve()}"',
        ])


def get_validator_model() -> type[BaseCardModel]:
    """Get the Pydantic validator class for this card type."""

    class CardModel(BaseCardTypeCustomFontAllText):        
        font_file: FilePath = HorizonTitleCard.CardConfig.font_file
        font_color: str = HorizonTitleCard.CardConfig.font_color
        font_size: FontSize = 1.0
        stroke_color: str = 'black'
        episode_text_vertical_shift: int = 0
        episode_text_font: FilePath = HorizonTitleCard.EPISODE_TEXT_FONT
        episode_text_color: str | None = None
        episode_text_font_size: FontSize = 1.0
        episode_text_stroke_color: str | None = None
        episode_text_kerning: int = 0
        episode_text_interword_spacing: int = 0
        separator: str = '•'
        separator_image_padding: int = 0
        separator_image_height: Annotated[int, Field(ge=10)] = 100
        separator_image_y_offset: int = 0
        separator_image_use_stroke: bool = True
        h_align: Literal['left', 'center', 'right'] = 'left'
        symbol: None | Literal[
            'acolyte',
            'ashoka',
            'andor',
            'bobafett',
            'mandalorian',
            'obiwan',
            'witcher',
            'logo',
        ] = None
        symbol_opacity: int = 100
        logo_file: Path | None = None
        crt_overlay: Literal['nobezel', 'bezel'] | None = None
        crt_state_overlay: bool = False
        omit_gradient: bool = True
        watched: bool | None = None

        @field_validator('episode_text_font', mode='before')
        @classmethod
        def validate_episode_text_font(cls, v, info):
            if v in ('{title_font}', '{font_file}'):
                v = info.data['font_file']
            etf = Path(v)
            # Episode text font does not exist, search alongside source image
            if not etf.exists():
                source_file = info.data.get('source_file')
                if source_file is not None:
                    candidate = Path(source_file).parent / etf.name
                    if candidate.exists():
                        v = candidate
                        etf = candidate
            # Verify new specified font file does exist
            etf = Path(v)
            if not etf.exists():
                raise ValueError(f'Specified Episode Text Font "{etf}" does not exist')
            return str(etf)

        @field_validator('separator', mode='before')
        @classmethod
        def validate_separator(cls, v, info):
            # Allow a single character as separator
            if isinstance(v, str) and len(v) == 1:
                return v
            # If it's a string that looks like a path, or a Path, try to resolve it
            sep_path = Path(v)
            if not sep_path.exists():
                source_file = info.data.get('source_file')
                if source_file is not None:
                    candidate = Path(source_file).parent / sep_path.name
                    if candidate.exists():
                        sep_path = candidate
            if not sep_path.exists():
                raise ValueError(f'Separator must be a single character or a valid image path "{v}" is invalid')
            return str(sep_path)

        @model_validator(mode='after')
        def assign_unassigned_colors(self) -> Self:
            """Assign any unassigned colors to their fallback values."""
            if self.episode_text_color is None:
                self.episode_text_color = self.font_color
            if self.episode_text_stroke_color is None:
                self.episode_text_stroke_color = self.stroke_color
            return self

    return CardModel

HorizonTitleCard.CardModel = get_validator_model()