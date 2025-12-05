# DawnTitleCard

## Description
This is a custom CardType that produces title cards with left, centered or right aligned text on the bottom. CRT TV overlay (nobezel or bezel) with optional watched style based on Yozora's Retro title card for shows like Stranger Things with a retro theme.

## Specification
Below is a table of all valid series [extras](https://github.com/CollinHeist/TitleCardMaker/wiki/Series-YAML-Files#extras) parsed by this card.

| Label | Default Value | Description |
| :---: | :---: | :--- |
| `stroke_color` | `black` | Stroke color of episode and title text |
| ~~`title_text_horizontal_shift`~~ | ~~`0`~~ | No longer required, title_text is trimmed automatically to align with episode text |
| `episode_text_vertical_shift` | `0` | How many pixels to vertically shift the episode text |
| `episode_text_font` | `Default` | Font file to use for the episode text |
| `episode_text_font_size` | `1.0` | Scalar of the size of the episode text |
| `episode_text_color` | `None` | Color to use separately for the episode text |
| `episode_text_stroke_color` | `None` | Color to use separately for the episode text stroke |
| `episode_text_kerning` | `0` | Pixel spacing between characters for the episode text |
| `episode_text_interword_spacing` | `0` | Spacing between words for the episode text |
| `separator` | `•` | Single character or image to separate the season and episode text.<br>Example: `image.png` to use the shows source folder or `/path/to/image.png` to use full path to image |
| `separator_image_padding` | `0` | Additional padding to apply to the left and right of the separator image if used |
| `separator_image_height` | `100` | Adjusts the height of the separator image if used keeping aspect ratio |
| `separator_image_y_offset` | `0` | Adjusts the vertical position of the separator image if used |
| `separator_image_use_stroke` | `True` | Automatically apply a stroke to the separator image to match text stroke width of text |
| `h_align` | `left` | Horizontal alignment. `left`, `center` or `right` |
| `crt_overlay` | `None` | Enable CRT TV Overlay `none`, `nobezel` or `bezel` |
| `crt_state_overlay` | `False` | Enable CRT TV Overlay watched/unwatched state `true`/`false` |
| `omit_gradient` | `True` | Omit gradient overlay `true`/`false` |

## Example Cards
<img src="https://raw.githubusercontent.com/Supremicus/tcm-images/main/Preview%20Cards/dawn-preview-card-ver2.jpg" width="1000"/>

## Features
- Left, Centered or Right side alignment
- Adjustable Episode text vertical offset for custom fonts.
- ~~Adjustable Title text horizontal offset for custom fonts.~~ Is now automatically trimmed.
- CRT TV overlay with a bezel or no bezel, with optional watched style (off by default)
- Optional Gradient
- **NEW**: Separator can now be a single character or an image

<br>

# HorizonTitleCard
## Description
This is a custom CardType that produces title cards similar to the left or right aligned with vertically centered text with optional symbol similar to the custom cards found on MediUX. CRT TV overlay (nobezel or bezel) with optional watched style based on Yozora's Retro title card for shows like Stranger Things with a retro theme.

## Specification
Below is a table of all valid series [extras](https://github.com/CollinHeist/TitleCardMaker/wiki/Series-YAML-Files#extras) parsed by this card.

| Label | Default Value | Description |
| :---: | :---: | :--- |
| `stroke_color` | `black` | Stroke color of episode and title text |
| `episode_text_vertical_shift` | `0` | How many pixels to vertically shift the episode text |
| `episode_text_font` | `Default` | Font file to use for the episode text |
| `episode_text_font_size` | `1.0` | Scalar of the size of the episode text |
| `episode_text_color` | `None` | Color to use separately for the episode text |
| `episode_text_stroke_color` | `None` | Color to use separately for the episode text stroke |
| `episode_text_kerning` | `0` | Pixel spacing between characters for the episode text |
| `episode_text_interword_spacing` | `0` | Spacing between words for the episode text |
| `separator` | `•` | Single character or image to separate the season and episode text.<br>Example: `image.png` to use the shows source folder or `/path/to/image.png` to use full path to image |
| `separator_image_padding` | `0` | Additional padding to apply to the left and right of the separator image if used |
| `separator_image_height` | `100` | Adjusts the height of the separator image if used keeping aspect ratio |
| `separator_image_y_offset` | `0` | Adjusts the vertical position of the separator image if used |
| `separator_image_use_stroke` | `True` | Automatically apply a stroke to the separator image to match text stroke width of text |
| `h_align` | `left` | Horizontal alignment. `left`, `center` or `right` |
| `symbol` | `None` | Custom symbol to use<br>Built-in: `acolyte`, `ahsoka`, `andor`, `bobafett`, `mandalorian`, `obiwan`, `witcher`<br>Custom: `logo` uses *source/show/logo.png* |
| `symbol_opacity` | `100` | Adjust opacity of the symbol. `100`% to `0`% |
| `crt_overlay` | `None` | Enable CRT TV Overlay `none`, `nobezel` or `bezel` |
| `crt_state_overlay` | `False` | Enable CRT TV Overlay watched/unwatched state `true`/`false` |
| `omit_gradient` | `True` | Omit gradient overlay `true`/`false` |
| ~~`alignment_overlay`~~ | ~~`False`~~ | No longer used. Now horizontally centers automatically |

## Example Cards
<img src="https://raw.githubusercontent.com/Supremicus/tcm-images/main/Preview%20Cards/horizon-preview-card-ver2.jpg" width="1000"/>

## Features
- Left, Centered or Right side alignment
- Built-in symbols for some shows, with the option to use your own custom symbols (uses logo.png in show source).
- Adjustable Episode text vertical offset for custom fonts.
- ~~Alignment overlay to adjust custom fonts if not using the default font.~~ Now horizontally centers automatically
- CRT TV overlay with a bezel or no bezel, with optional watched style (off by default)
- Optional Radial Gradient
- **NEW**: Separator can now be a single character or an image