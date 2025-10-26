from pathlib import Path
from typing import Annotated, Any

from pydantic import StringConstraints

from app.cards.base import BaseCardType, CardTypeDescription, DefaultCardConfig
from app.cards.loader import RemoteFile
from app.schemas.card_type import BaseCardTypeCustomFontNoText


class StarWarsTitleOnly(BaseCardType):
    """
    This class describes a type of Card that produces a modified version
    of the Star Wars card.
    """

    API_DETAILS = CardTypeDescription(
        name='Star Wars (Title Only)',
        identifier='Wdvh/StarWarsTitleOnly',
        example=(
            'https://user-images.githubusercontent.com/17693271/'
            '178131539-c7b55ced-b9ba-4564-8153-a998454e1742.jpg'
        ),
        creators=['Wdvh', 'CollinHeist'],
        source='remote',
        supports_custom_fonts=False,
        supports_custom_seasons=False,
        supported_extras=[],
        description=[
            'A variation of the standard Star Wars Card for Shows like '
            'Obi-Wan Kenobi that use Part/Chapter and similar as episode '
            'titles.', 'This card also uses a modified star gradient so that '
            'more of the left side of the image is visible.',
        ]
    )

    class CardModel(BaseCardTypeCustomFontNoText):
        title_text: Annotated[str, StringConstraints(to_upper=True)]
        font_color: str = '#DAC960'

    """Directory where all reference files used by this card are stored"""
    REF_DIRECTORY = Path(__file__).parent.parent / 'ref' / 'star_wars'

    CardConfig = DefaultCardConfig(
        font_file=REF_DIRECTORY / 'Monstice-Base.ttf',
        font_color='#DAC960',
        font_replacements={'Ō': 'O', 'ō': 'o'},
        title_max_line_width=16,
        title_max_line_count=5,
        title_split_style='top',
        episode_text_format=' ',
    )

    """Path to the reference star image to overlay on all source images"""
    __STAR_GRADIENT_IMAGE = RemoteFile('Wdvh', 'star_gradient_title_only.png')

    __slots__ = ('source_file', 'output_file', 'title')

    
    def __init__(self, *,
            source_file: Path,
            card_file: Path,
            title_text: str,
            blur: bool = False,
            grayscale: bool = False,
            **unused: Any,
        ) -> None:
        """Initialize this CardType object."""
        
        super().__init__(blur, grayscale)

        self.source_file = source_file
        self.output_file = card_file
        self.title = self.image_magick.escape_chars(title_text)


    def create(self) -> None:
        """Create this object's defined title card."""

        self.image_magick.run([
            f'convert "{self.source_file.resolve()}"',
            # Resize input and apply any style modifiers
            *self.resize_and_style,
            # Overlay the star gradient
            f'"{self.__STAR_GRADIENT_IMAGE.resolve()}"',
            f'-composite',
            # Add title text
            f'-font "{self.CardConfig.font_file.resolve()}"',
            f'-gravity northwest',
            f'-pointsize 124',
            f'-kerning 0.5',
            f'-interline-spacing 20',
            f'-fill "{self.CardConfig.font_color}"',
            f'-annotate +320+1529 "{self.title}"',
            # Attempt to overlay mask
            *self.add_overlay_mask(self.source_file),
            # Resize and write output
            *self.resize_output,
            f'"{self.output_file.resolve()}"',
        ])
