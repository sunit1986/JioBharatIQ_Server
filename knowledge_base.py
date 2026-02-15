"""
JDS Knowledge Base - Sanitized data extracted from CLAUDE.md and memory files.
No file paths, no internal reasoning, strict structure only.
"""

# Component Specifications
COMPONENTS = {
    "Button": {
        "name": "Button",
        "import_path": "@jds/core",
        "description": "Primary interactive element for user actions",
        "kinds": ["primary", "secondary", "tertiary"],
        "sizes": ["small", "medium", "large"],
        "states": ["normal", "positive", "disabled", "loading"],
        "props": {
            "kind": {
                "type": "string",
                "options": ["primary", "secondary", "tertiary"],
                "default": "primary",
                "description": "Visual style variant"
            },
            "size": {
                "type": "string",
                "options": ["small", "medium", "large"],
                "default": "medium",
                "description": "Button size"
            },
            "label": {
                "type": "string",
                "required": True,
                "description": "Button text label"
            },
            "icon": {
                "type": "ReactNode",
                "description": "Icon element (right side)"
            },
            "iconLeft": {
                "type": "ReactNode",
                "description": "Icon element (left side)"
            },
            "fullWidth": {
                "type": "boolean",
                "default": False,
                "description": "Expand to full container width"
            },
            "disabled": {
                "type": "boolean",
                "default": False,
                "description": "Disable interaction"
            },
            "loading": {
                "type": "boolean",
                "default": False,
                "description": "Show loading state"
            },
            "state": {
                "type": "string",
                "options": ["normal", "positive"],
                "default": "normal",
                "description": "Visual state"
            },
            "onClick": {
                "type": "function",
                "description": "Click handler"
            }
        },
        "code_example": """import { Button } from '@jds/core';

<Button
  kind="primary"
  size="medium"
  label="Click me"
  onClick={() => {}}
/>"""
    },
    "InputField": {
        "name": "InputField",
        "import_path": "@jds/core",
        "description": "Text input field with validation states",
        "types": ["text", "email", "password", "number"],
        "states": ["none", "success", "warning", "error"],
        "props": {
            "type": {
                "type": "string",
                "options": ["text", "email", "password", "number"],
                "default": "text",
                "description": "Input type"
            },
            "label": {
                "type": "string",
                "description": "Field label"
            },
            "helperText": {
                "type": "string",
                "description": "Helper text below field"
            },
            "state": {
                "type": "string",
                "options": ["none", "success", "warning", "error"],
                "default": "none",
                "description": "Validation state"
            },
            "stateText": {
                "type": "string",
                "description": "Validation message"
            },
            "prefix": {
                "type": "ReactNode",
                "description": "Leading icon/element"
            },
            "suffix": {
                "type": "ReactNode",
                "description": "Trailing icon/element"
            },
            "placeholder": {
                "type": "string",
                "description": "Placeholder text"
            },
            "value": {
                "type": "string",
                "description": "Input value"
            },
            "onChange": {
                "type": "function",
                "description": "Change handler"
            }
        },
        "code_example": """import { InputField } from '@jds/core';

<InputField
  type="text"
  label="Email"
  placeholder="Enter your email"
  state="none"
  value={value}
  onChange={(e) => setValue(e.target.value)}
/>"""
    },
    "Card": {
        "name": "Card",
        "import_path": "@jds/core",
        "description": "Container for grouping related content",
        "orientations": ["vertical", "horizontal"],
        "sizes": ["xtra-small", "xxs", "small", "medium", "large"],
        "image_ratios": ["square", "wide", "landscape", "portrait"],
        "props": {
            "title": {
                "type": "string",
                "description": "Card title"
            },
            "description": {
                "type": "string",
                "description": "Card description text"
            },
            "caption": {
                "type": "string",
                "description": "Caption text"
            },
            "image": {
                "type": "string",
                "description": "Image URL"
            },
            "imageFocus": {
                "type": "string",
                "options": ["center", "top", "bottom", "left", "right"],
                "default": "center",
                "description": "Image focus point"
            },
            "imageRatio": {
                "type": "string",
                "options": ["square", "wide", "landscape", "portrait"],
                "default": "square",
                "description": "Image aspect ratio"
            },
            "primaryCTA": {
                "type": "string",
                "description": "Primary button label"
            },
            "secondaryCTA": {
                "type": "string",
                "description": "Secondary button label"
            },
            "orientation": {
                "type": "string",
                "options": ["vertical", "horizontal"],
                "default": "vertical",
                "description": "Layout orientation"
            }
        },
        "code_example": """import { Card } from '@jds/core';

<Card
  title="Card Title"
  description="Description text"
  image="https://example.com/image.jpg"
  primaryCTA="Learn More"
  orientation="vertical"
/>"""
    },
    "Modal": {
        "name": "Modal",
        "import_path": "@jds/core",
        "description": "Overlay dialog for focused interactions",
        "sizes": ["small", "medium", "large", "xlarge"],
        "props": {
            "isOpen": {
                "type": "boolean",
                "required": True,
                "description": "Modal visibility state"
            },
            "onClose": {
                "type": "function",
                "required": True,
                "description": "Close handler"
            },
            "title": {
                "type": "string",
                "description": "Modal title"
            },
            "size": {
                "type": "string",
                "options": ["small", "medium", "large", "xlarge"],
                "default": "medium",
                "description": "Modal size"
            },
            "children": {
                "type": "ReactNode",
                "description": "Modal content"
            }
        },
        "code_example": """import { Modal } from '@jds/core';

<Modal
  isOpen={isOpen}
  onClose={() => setIsOpen(false)}
  title="Modal Title"
  size="medium"
>
  <p>Modal content</p>
</Modal>"""
    },
    "BottomSheet": {
        "name": "BottomSheet",
        "import_path": "@jds/core",
        "description": "Mobile-optimized bottom drawer",
        "states": ["closed", "peek", "half", "full"],
        "props": {
            "isOpen": {
                "type": "boolean",
                "required": True,
                "description": "Sheet visibility"
            },
            "onClose": {
                "type": "function",
                "description": "Close handler"
            },
            "defaultState": {
                "type": "string",
                "options": ["peek", "half", "full"],
                "default": "half",
                "description": "Initial open state"
            },
            "children": {
                "type": "ReactNode",
                "description": "Sheet content"
            }
        },
        "code_example": """import { BottomSheet } from '@jds/core';

<BottomSheet
  isOpen={isOpen}
  onClose={() => setIsOpen(false)}
  defaultState="half"
>
  <div>Content</div>
</BottomSheet>"""
    },
    "Avatar": {
        "name": "Avatar",
        "import_path": "@jds/core",
        "description": "User profile picture or initials",
        "kinds": ["image", "initials", "icon"],
        "sizes": ["xsmall", "small", "medium", "large", "xlarge"],
        "props": {
            "kind": {
                "type": "string",
                "options": ["image", "initials", "icon"],
                "required": True,
                "description": "Avatar type"
            },
            "size": {
                "type": "string",
                "options": ["xsmall", "small", "medium", "large", "xlarge"],
                "default": "medium",
                "description": "Avatar size"
            },
            "image": {
                "type": "string",
                "description": "Image URL (for kind=image)"
            },
            "initials": {
                "type": "string",
                "description": "Initials text (for kind=initials)"
            },
            "icon": {
                "type": "ReactNode",
                "description": "Icon element (for kind=icon)"
            }
        },
        "code_example": """import { Avatar } from '@jds/core';

<Avatar
  kind="initials"
  size="medium"
  initials="JD"
/>"""
    },
    "Tabs": {
        "name": "Tabs",
        "import_path": "@jds/core",
        "description": "Navigation tabs for content sections",
        "overflow_options": ["fit", "scroll", "arrows"],
        "props": {
            "items": {
                "type": "array",
                "required": True,
                "description": "Array of tab objects [{label: string}]"
            },
            "activeTab": {
                "type": "number",
                "default": 0,
                "description": "Active tab index"
            },
            "overflow": {
                "type": "string",
                "options": ["fit", "scroll", "arrows"],
                "default": "fit",
                "description": "Overflow behavior"
            },
            "appearance": {
                "type": "string",
                "default": "normal",
                "description": "Visual appearance"
            },
            "fullWidth": {
                "type": "boolean",
                "default": False,
                "description": "Expand tabs to full width"
            },
            "background": {
                "type": "boolean",
                "default": False,
                "description": "Show background"
            },
            "onChange": {
                "type": "function",
                "description": "Tab change handler (index) => void"
            }
        },
        "code_example": """import { Tabs } from '@jds/core';

<Tabs
  items={[
    { label: 'Home' },
    { label: 'Magazines' },
    { label: 'News Papers' }
  ]}
  activeTab={0}
  overflow="fit"
  onChange={(index) => setActive(index)}
/>"""
    },
    "Toast": {
        "name": "Toast",
        "import_path": "@jds/core",
        "description": "Temporary notification messages",
        "props": {
            "title": {
                "type": "string",
                "required": True,
                "description": "Toast title"
            },
            "description": {
                "type": "string",
                "description": "Toast description"
            },
            "dismissAfter": {
                "type": "number",
                "default": 5000,
                "description": "Auto-dismiss in milliseconds"
            },
            "primaryCTA": {
                "type": "object",
                "description": "Primary action {title: string}"
            },
            "secondaryCTA": {
                "type": "object",
                "description": "Secondary action {title: string}"
            },
            "icon": {
                "type": "ReactNode",
                "description": "Leading icon"
            },
            "open": {
                "type": "boolean",
                "default": True,
                "description": "Toast visibility"
            },
            "showClose": {
                "type": "boolean",
                "default": True,
                "description": "Show close button"
            },
            "onClose": {
                "type": "function",
                "description": "Close handler"
            }
        },
        "code_example": """import { Toast } from '@jds/core';

<Toast
  title="Success!"
  description="Your changes have been saved."
  dismissAfter={3000}
  onClose={() => {}}
/>"""
    },
    "Accordion": {
        "name": "Accordion",
        "import_path": "@jds/core",
        "description": "Expandable/collapsible content panels",
        "icon_types": ["chevron", "plus"],
        "props": {
            "iconType": {
                "type": "string",
                "options": ["chevron", "plus"],
                "default": "chevron",
                "description": "Expand/collapse icon type"
            },
            "allowMultiple": {
                "type": "boolean",
                "default": False,
                "description": "Allow multiple panels open"
            },
            "expanded": {
                "type": "array",
                "description": "Array of expanded panel indices"
            },
            "onChange": {
                "type": "function",
                "description": "Expansion change handler"
            }
        },
        "sub_components": {
            "AccordionPanel": {
                "props": {
                    "header": {"type": "string", "description": "Panel header text"},
                    "subtitle": {"type": "string", "description": "Panel subtitle"},
                    "disabled": {"type": "boolean", "default": False, "description": "Disable panel"},
                    "children": {"type": "ReactNode", "description": "Panel content"}
                }
            }
        },
        "code_example": """import { Accordion, AccordionPanel } from '@jds/core';

<Accordion iconType="chevron" allowMultiple={false}>
  <AccordionPanel header="Panel 1" subtitle="Subtitle">
    Content here
  </AccordionPanel>
  <AccordionPanel header="Panel 2">
    More content
  </AccordionPanel>
</Accordion>"""
    },
    "Divider": {
        "name": "Divider",
        "import_path": "@jds/core",
        "description": "Visual separator between content sections",
        "props": {
            "orientation": {
                "type": "string",
                "options": ["horizontal", "vertical"],
                "default": "horizontal",
                "description": "Divider direction"
            },
            "label": {
                "type": "string",
                "description": "Optional label text (e.g., 'OR')"
            },
            "pad": {
                "type": "string",
                "default": "medium",
                "description": "Padding size"
            },
            "padPosition": {
                "type": "string",
                "options": ["all", "left", "right", "top", "bottom"],
                "default": "all",
                "description": "Padding position"
            }
        },
        "code_example": """import { Divider } from '@jds/core';

<Divider />
<Divider label="OR" />
<Divider orientation="vertical" />"""
    },
    "Badge": {
        "name": "Badge",
        "import_path": "@jds/core",
        "description": "Small status or label indicator",
        "kinds": ["normal", "service"],
        "sizes": ["small", "medium", "large"],
        "badge_types": ["notification", "status", "informational", "brand"],
        "props": {
            "label": {
                "type": "string",
                "required": True,
                "description": "Badge text"
            },
            "kind": {
                "type": "string",
                "options": ["normal", "service"],
                "default": "normal",
                "description": "Badge type"
            },
            "size": {
                "type": "string",
                "options": ["small", "medium", "large"],
                "default": "medium",
                "description": "Badge size"
            },
            "icon": {
                "type": "ReactNode",
                "description": "Optional icon"
            }
        },
        "code_example": """import { Badge } from '@jds/core';
import { IcFavorite } from '@jds/core-icons';

<Badge kind="normal" label="NEW" size="medium" />
<Badge kind="service" label="Saavn" icon={<PsJioSaavn />} />"""
    },
    "BottomNav": {
        "name": "BottomNav",
        "import_path": "@jds/core",
        "description": "Bottom navigation bar for mobile apps",
        "props": {
            "items": {
                "type": "array",
                "required": True,
                "description": "Nav items [{icon, title?, disabled?}]"
            },
            "activeIndex": {
                "type": "number",
                "default": 0,
                "description": "Active item index"
            },
            "showLabel": {
                "type": "boolean",
                "default": True,
                "description": "Show item labels"
            },
            "multiLine": {
                "type": "boolean",
                "default": False,
                "description": "Allow multi-line labels"
            },
            "onChange": {
                "type": "function",
                "description": "Navigation handler (index) => void"
            }
        },
        "code_example": """import { BottomNav } from '@jds/core';

<BottomNav
  items={[
    { icon: 'ic_home', title: 'Home' },
    { icon: 'ic_favorite', title: 'Favorite' },
    { icon: 'ic_camera', title: 'Camera' },
    { icon: 'ic_downloads', title: 'Downloads' }
  ]}
  activeIndex={0}
  showLabel={true}
  onChange={(index) => setActive(index)}
/>"""
    },
    "Container": {
        "name": "Container",
        "import_path": "@jds/core",
        "description": "Flexible layout container with alignment and spacing",
        "props": {
            "verticalAlign": {
                "type": "string",
                "options": ["start", "center", "end"],
                "default": "start",
                "description": "Vertical alignment"
            },
            "horizontalAlign": {
                "type": "string",
                "options": ["start", "center", "end"],
                "default": "start",
                "description": "Horizontal alignment"
            },
            "direction": {
                "type": "string",
                "options": ["row", "column"],
                "default": "row",
                "description": "Layout direction"
            },
            "gap": {
                "type": "string",
                "description": "Gap between children"
            },
            "width": {
                "type": "string",
                "description": "Container width"
            },
            "height": {
                "type": "string",
                "description": "Container height"
            },
            "fullWidth": {
                "type": "boolean",
                "default": False,
                "description": "Full width container"
            },
            "overflow": {
                "type": "string",
                "options": ["visible", "hidden", "scroll", "auto"],
                "default": "visible",
                "description": "Overflow behavior"
            }
        },
        "code_example": """import { Container } from '@jds/core';

<Container
  direction="column"
  gap="16"
  verticalAlign="center"
  horizontalAlign="center"
>
  {children}
</Container>"""
    },
    "Spinner": {
        "name": "Spinner",
        "import_path": "@jds/core",
        "description": "Loading indicator",
        "kinds": ["normal", "inline", "vibrant"],
        "sizes": ["small", "medium"],
        "props": {
            "kind": {
                "type": "string",
                "options": ["normal", "inline", "vibrant"],
                "default": "normal",
                "description": "Visual style"
            },
            "size": {
                "type": "string",
                "options": ["small", "medium"],
                "default": "medium",
                "description": "Spinner size"
            },
            "label": {
                "type": "string",
                "description": "Loading text"
            },
            "labelPosition": {
                "type": "string",
                "options": ["right", "bottom"],
                "default": "right",
                "description": "Label placement"
            },
            "isOverlay": {
                "type": "boolean",
                "default": False,
                "description": "Show as overlay"
            }
        },
        "code_example": """import { Spinner } from '@jds/core';

<Spinner kind="normal" size="medium" label="Loading..." />"""
    },
    "Skeleton": {
        "name": "Skeleton",
        "import_path": "@jds/core",
        "description": "Content placeholder during loading",
        "shapes": ["circle", "rectangle", "square", "heading", "paragraph"],
        "props": {
            "shape": {
                "type": "string",
                "options": ["circle", "rectangle", "square", "heading", "paragraph"],
                "required": True,
                "description": "Skeleton shape"
            },
            "width": {
                "type": "number",
                "description": "Container width"
            },
            "animated": {
                "type": "boolean",
                "default": True,
                "description": "Enable shimmer animation"
            }
        },
        "code_example": """import { Skeleton } from '@jds/core';

<Skeleton shape="rectangle" width={200} animated={true} />
<Skeleton shape="circle" width={48} />"""
    },
    "PromoCard": {
        "name": "PromoCard",
        "import_path": "@jds/core",
        "description": "Promotional content card with rich media",
        "orientations": ["vertical", "horizontal"],
        "sizes": ["default", "compact"],
        "image_ratios": ["wide", "square", "landscape", "portrait"],
        "props": {
            "title": {
                "type": "string",
                "required": True,
                "description": "Promo title"
            },
            "description": {
                "type": "string",
                "description": "Promo description"
            },
            "image": {
                "type": "string",
                "description": "Image URL"
            },
            "primaryCTA": {
                "type": "string",
                "description": "Action button label"
            },
            "orientation": {
                "type": "string",
                "options": ["vertical", "horizontal"],
                "default": "vertical",
                "description": "Layout orientation"
            },
            "imageRatio": {
                "type": "string",
                "options": ["wide", "square", "landscape", "portrait"],
                "default": "wide",
                "description": "Image aspect ratio"
            },
            "size": {
                "type": "string",
                "options": ["default", "compact"],
                "default": "default",
                "description": "Card size"
            },
            "shadow": {
                "type": "boolean",
                "default": False,
                "description": "Show card shadow"
            }
        },
        "code_example": """import { PromoCard } from '@jds/core';

<PromoCard
  title="Take your news everywhere"
  description="Subscribe now"
  image="images/promo.png"
  primaryCTA="Get Now"
  orientation="vertical"
  imageRatio="wide"
/>"""
    },
    "ServiceCard": {
        "name": "ServiceCard",
        "import_path": "@jds/core",
        "description": "Card for service/product display with branding",
        "sizes": ["s", "xs", "xxs"],
        "image_ratios": ["wide", "square", "landscape", "portrait"],
        "props": {
            "title": {
                "type": "string",
                "required": True,
                "description": "Service title"
            },
            "description": {
                "type": "string",
                "description": "Service description"
            },
            "image": {
                "type": "string",
                "description": "Service image URL"
            },
            "primaryCTA": {
                "type": "string",
                "description": "Action button label"
            },
            "size": {
                "type": "string",
                "options": ["s", "xs", "xxs"],
                "default": "s",
                "description": "Card size"
            },
            "caption": {
                "type": "object",
                "description": "Service badge {label, icon}"
            }
        },
        "code_example": """import { ServiceCard } from '@jds/core';

<ServiceCard
  title="With Love, from Jio"
  description="Support text line"
  image="https://example.com/image.jpg"
  primaryCTA="Get"
  size="s"
  caption={{ label: "Saavn", icon: "ps_jio_saavn" }}
/>"""
    },
    "ContentBlock": {
        "name": "ContentBlock",
        "import_path": "@jds/core",
        "description": "Structured content section with heading and CTAs",
        "sizes": ["xxs", "xs", "s", "m", "l", "xl"],
        "props": {
            "size": {
                "type": "string",
                "options": ["xxs", "xs", "s", "m", "l", "xl"],
                "default": "m",
                "description": "Content block size"
            },
            "caption": {
                "type": "string",
                "description": "Caption text"
            },
            "title": {
                "type": "string",
                "required": True,
                "description": "Block title"
            },
            "description": {
                "type": "string",
                "description": "Block description"
            },
            "primaryCTA": {
                "type": "string",
                "description": "Primary action label"
            },
            "secondaryCTA": {
                "type": "string",
                "description": "Secondary action label"
            },
            "invertCTA": {
                "type": "boolean",
                "default": False,
                "description": "Swap CTA positions"
            },
            "ctaWrap": {
                "type": "string",
                "options": ["horizontal", "vertical"],
                "default": "horizontal",
                "description": "CTA layout direction"
            }
        },
        "code_example": """import { ContentBlock } from '@jds/core';

<ContentBlock
  size="m"
  title="Section Title"
  description="Description text"
  primaryCTA="Get Now"
  secondaryCTA="Learn More"
/>"""
    },
    "Carousel": {
        "name": "Carousel",
        "import_path": "@jds/core",
        "description": "Horizontal content slider with indicators",
        "indicator_types": ["dot", "none", "label", "dot with label"],
        "density_options": ["relaxed", "condensed"],
        "props": {
            "showArrows": {
                "type": "boolean",
                "default": True,
                "description": "Show navigation arrows"
            },
            "indicatorType": {
                "type": "string",
                "options": ["dot", "none", "label", "dot with label"],
                "default": "dot",
                "description": "Slide indicator type"
            },
            "density": {
                "type": "string",
                "options": ["relaxed", "condensed"],
                "default": "relaxed",
                "description": "Spacing density"
            },
            "autoPlay": {
                "type": "boolean",
                "default": False,
                "description": "Auto-advance slides"
            },
            "showPlayPause": {
                "type": "boolean",
                "default": False,
                "description": "Show play/pause control"
            },
            "children": {
                "type": "ReactNode",
                "description": "Slide content elements"
            }
        },
        "code_example": """import { Carousel } from '@jds/core';

<Carousel indicatorType="dot" density="relaxed" showArrows={true}>
  <Card title="Card 1" />
  <Card title="Card 2" />
  <Card title="Card 3" />
</Carousel>"""
    },
    "RatingBar": {
        "name": "RatingBar",
        "import_path": "@jds/core",
        "description": "Star rating input and display",
        "types": ["interactive", "read_only_expanded", "read_only_compact"],
        "sizes": ["small", "medium", "large"],
        "props": {
            "type": {
                "type": "string",
                "options": ["interactive", "read_only_expanded", "read_only_compact"],
                "default": "interactive",
                "description": "Rating bar behavior"
            },
            "size": {
                "type": "string",
                "options": ["small", "medium", "large"],
                "default": "medium",
                "description": "Star size"
            },
            "value": {
                "type": "number",
                "required": True,
                "description": "Current rating value"
            },
            "maxValue": {
                "type": "number",
                "default": 5,
                "description": "Maximum rating"
            },
            "label": {
                "type": "string",
                "description": "Rating label"
            },
            "labelPosition": {
                "type": "string",
                "options": ["top_left", "top_center", "bottom_left", "bottom_center", "left", "right"],
                "default": "top_left",
                "description": "Label placement"
            },
            "onChange": {
                "type": "function",
                "description": "Rating change handler"
            }
        },
        "code_example": """import { RatingBar } from '@jds/core';

<RatingBar
  type="interactive"
  size="medium"
  value={3}
  maxValue={5}
  onChange={(value) => setRating(value)}
/>"""
    },
    "Text": {
        "name": "Text",
        "import_path": "@jds/core",
        "description": "Typography component for all text rendering",
        "variants": ["body", "label", "title", "headline", "display"],
        "sizes": ["4XS", "3XS", "2XS", "XS", "S", "M", "L", "XL", "2XL"],
        "weights": ["low", "medium", "high"],
        "appearances": ["primary", "secondary", "sparkle", "neutral", "positive", "warning", "negative", "informative"],
        "props": {
            "text": {
                "type": "string",
                "required": True,
                "description": "Text content"
            },
            "variant": {
                "type": "string",
                "options": ["body", "label", "title", "headline", "display"],
                "default": "body",
                "description": "Typography variant"
            },
            "size": {
                "type": "string",
                "options": ["4XS", "3XS", "2XS", "XS", "S", "M", "L", "XL", "2XL"],
                "default": "M",
                "description": "Text size"
            },
            "weight": {
                "type": "string",
                "options": ["low", "medium", "high"],
                "default": "medium",
                "description": "Font weight"
            },
            "attention": {
                "type": "string",
                "options": ["low", "medium", "high"],
                "default": "high",
                "description": "Visual emphasis"
            },
            "appearance": {
                "type": "string",
                "options": ["neutral", "primary", "secondary", "sparkle", "positive", "negative", "warning", "informative"],
                "default": "neutral",
                "description": "Semantic appearance"
            },
            "textAlign": {
                "type": "string",
                "options": ["left", "center", "right"],
                "default": "left",
                "description": "Text alignment"
            },
            "maxLines": {
                "type": "number",
                "description": "Max lines before truncation"
            },
            "strikethrough": {
                "type": "boolean",
                "default": False,
                "description": "Strikethrough decoration"
            },
            "italic": {
                "type": "boolean",
                "default": False,
                "description": "Italic style"
            },
            "underline": {
                "type": "boolean",
                "default": False,
                "description": "Underline decoration"
            }
        },
        "code_example": """import { Text } from '@jds/core';

<Text
  text="Hello World"
  variant="headline"
  size="L"
  weight="high"
  appearance="primary"
/>"""
    }
}

# Design Tokens
TOKENS = {
    "colors": {
        "primary": {
            "primary-20": {"value": "#e8e8fc", "usage": "Light backgrounds, hover states"},
            "primary-30": {"value": "#9999ff", "usage": "Disabled states, borders"},
            "primary-40": {"value": "#6464ff", "usage": "Secondary actions"},
            "primary-50": {"value": "#3535f3", "usage": "Primary brand color, main actions"},
            "primary-60": {"value": "#000093", "usage": "Links, focus states"},
            "primary-70": {"value": "#00004c", "usage": "Pressed states, dark themes"},
            "primary-80": {"value": "#010029", "usage": "Deep backgrounds"}
        },
        "secondary": {
            "secondary-20": {"value": "#fef7e9", "usage": "Warning backgrounds"},
            "secondary-30": {"value": "#ffe3ae", "usage": "Light accents"},
            "secondary-40": {"value": "#ffd947", "usage": "Attention highlights"},
            "secondary-50": {"value": "#f7ab20", "usage": "Secondary brand color"},
            "secondary-60": {"value": "#ac660c", "usage": "Warnings, alerts"},
            "secondary-70": {"value": "#7f4b10", "usage": "Dark warning states"},
            "secondary-80": {"value": "#401d0c", "usage": "Deep warning backgrounds"}
        },
        "sparkle": {
            "sparkle-20": {"value": "#e8faf7", "usage": "Success backgrounds"},
            "sparkle-30": {"value": "#a7f6e9", "usage": "Light success states"},
            "sparkle-40": {"value": "#7aebd9", "usage": "Active success"},
            "sparkle-50": {"value": "#1eccb0", "usage": "Success indicators"},
            "sparkle-60": {"value": "#1e7b74", "usage": "Success text"},
            "sparkle-70": {"value": "#0e5c4f", "usage": "Dark success"},
            "sparkle-80": {"value": "#08332c", "usage": "Deep success backgrounds"}
        },
        "feedback": {
            "error": {"value": "#fa2F40", "usage": "Error states, destructive actions"},
            "warning": {"value": "#f06d0f", "usage": "Warning states, caution"},
            "success": {"value": "#25ab21", "usage": "Success states, confirmations"}
        },
        "grey": {
            "grey-100": {"value": "#141414", "usage": "Primary text, high emphasis"},
            "grey-80": {"value": "#000000a6", "usage": "Secondary text, 66% opacity"},
            "grey-60": {"value": "#b5b5b5", "usage": "Disabled text, placeholders"},
            "grey-40": {"value": "#e0e0e0", "usage": "Borders, dividers"},
            "grey-20": {"value": "#f5f5f5", "usage": "Background surfaces"}
        },
        "global": {
            "white": {"value": "#ffffff", "usage": "Light surfaces, text on dark"},
            "black": {"value": "#141414", "usage": "Dark surfaces, primary text"}
        }
    },
    "typography": {
        "heading": {
            "heading-xl": {
                "font": "JioType",
                "size": "88px",
                "line_height": "88px",
                "weight": "Black",
                "letter_spacing": "-3%",
                "usage": "Hero headings, page titles"
            },
            "heading-l": {
                "font": "JioType",
                "size": "64px",
                "line_height": "64px",
                "weight": "Black",
                "letter_spacing": "-3%",
                "usage": "Section headings"
            },
            "heading-m": {
                "font": "JioType",
                "size": "40px",
                "line_height": "40px",
                "weight": "Black",
                "letter_spacing": "-3%",
                "usage": "Card headings, subsections"
            },
            "heading-s": {
                "font": "JioType",
                "size": "32px",
                "line_height": "32px",
                "weight": "Black",
                "letter_spacing": "-3%",
                "usage": "Small headings"
            },
            "heading-xs": {
                "font": "JioType",
                "size": "24px",
                "line_height": "28px",
                "weight": "Black",
                "letter_spacing": "-3%",
                "usage": "Component headings"
            },
            "heading-xxs": {
                "font": "JioType",
                "size": "16px",
                "line_height": "20px",
                "weight": "Black",
                "letter_spacing": "-3%",
                "usage": "Minimal headings"
            }
        },
        "body": {
            "body-l": {
                "font": "JioType",
                "size": "24px",
                "line_height": "32px",
                "weight": "Medium",
                "letter_spacing": "-0.5%",
                "usage": "Lead paragraphs, blog text"
            },
            "body-m": {
                "font": "JioType",
                "size": "18px",
                "line_height": "24px",
                "weight": "Medium",
                "letter_spacing": "-0.5%",
                "usage": "Standard paragraphs"
            },
            "body-s": {
                "font": "JioType",
                "size": "16px",
                "line_height": "24px",
                "weight": "Medium",
                "letter_spacing": "-0.5%",
                "usage": "Body text, default"
            },
            "body-xs": {
                "font": "JioType",
                "size": "14px",
                "line_height": "20px",
                "weight": "Medium",
                "letter_spacing": "-0.5%",
                "usage": "Captions, labels"
            },
            "body-xxs": {
                "font": "JioType",
                "size": "12px",
                "line_height": "16px",
                "weight": "Medium",
                "letter_spacing": "-0.5%",
                "usage": "Small captions, legal text"
            },
            "body-3xs": {
                "font": "JioType",
                "size": "11px",
                "line_height": "14px",
                "weight": "Medium",
                "letter_spacing": "-0.5%",
                "usage": "Footer text, badges"
            }
        },
        "special": {
            "overline": {
                "font": "JioType",
                "size": "14px",
                "line_height": "16px",
                "weight": "Bold",
                "letter_spacing": "-0.5%",
                "case": "uppercase",
                "usage": "Overline labels"
            },
            "button": {
                "font": "JioType",
                "size": "16px",
                "line_height": "24px",
                "weight": "Bold",
                "letter_spacing": "-0.5%",
                "usage": "Button labels"
            },
            "label": {
                "font": "JioType",
                "size": "16px",
                "line_height": "20px",
                "weight": "Medium",
                "letter_spacing": "-0.5%",
                "usage": "List titles, form labels"
            },
            "code": {
                "font": "JetBrains Mono",
                "size": "12px",
                "line_height": "16px",
                "weight": "Regular",
                "letter_spacing": "0%",
                "usage": "Code snippets"
            }
        }
    },
    "spacing": {
        "xxs": {"value": "4px", "usage": "Minimal spacing"},
        "xs": {"value": "8px", "usage": "Tight spacing"},
        "s": {"value": "12px", "usage": "Small spacing"},
        "base": {"value": "16px", "usage": "Base spacing unit"},
        "m": {"value": "24px", "usage": "Medium spacing"},
        "l": {"value": "32px", "usage": "Large spacing"},
        "xl": {"value": "48px", "usage": "Extra large spacing"},
        "xxl": {"value": "64px", "usage": "Section spacing"},
        "huge": {"value": "96px", "usage": "Large section gaps"},
        "massive": {"value": "128px", "usage": "Hero section spacing"}
    },
    "border_radius": {
        "none": {"value": "0px", "usage": "Sharp corners"},
        "xSmall": {"value": "4px", "usage": "Minimal rounding"},
        "small": {"value": "8px", "usage": "Small rounding"},
        "medium": {"value": "12px", "usage": "Medium rounding"},
        "large": {"value": "16px", "usage": "Large rounding"},
        "xl": {"value": "20px", "usage": "Extra large rounding"},
        "xxl": {"value": "23px", "usage": "Input fields, cards"},
        "pill": {"value": "999px", "usage": "Fully rounded (pills, buttons)"}
    },
    "opacity": {
        "invisible": {"value": "0", "usage": "Hidden elements"},
        "disabled": {"value": "0.4", "usage": "Disabled state"},
        "enabled": {"value": "1", "usage": "Fully visible"}
    }
}

# Icon Categories (1546 icons across 15 categories)
ICON_CATEGORIES = {
    "communication": [
        "ic_mail", "ic_mail_outline", "ic_message", "ic_message_outline",
        "ic_chat", "ic_chat_outline", "ic_phone", "ic_phone_outline",
        "ic_video_call", "ic_videocam", "ic_notifications", "ic_notifications_outline"
    ],
    "media": [
        "ic_play", "ic_pause", "ic_stop", "ic_skip_next", "ic_skip_previous",
        "ic_volume_up", "ic_volume_down", "ic_volume_mute", "ic_mic", "ic_mic_off"
    ],
    "navigation": [
        "ic_arrow_back", "ic_arrow_forward", "ic_arrow_up", "ic_arrow_down",
        "ic_chevron_left", "ic_chevron_right", "ic_menu", "ic_more_vert", "ic_more_horiz",
        "ic_close", "ic_home", "ic_home_outline"
    ],
    "action": [
        "ic_search", "ic_settings", "ic_favorite", "ic_favorite_outline",
        "ic_add", "ic_remove", "ic_edit", "ic_delete", "ic_check", "ic_close",
        "ic_refresh", "ic_share", "ic_download", "ic_upload", "ic_save"
    ],
    "content": [
        "ic_add", "ic_remove", "ic_copy", "ic_cut", "ic_paste", "ic_undo", "ic_redo",
        "ic_link", "ic_attach", "ic_flag", "ic_filter", "ic_sort"
    ],
    "device": [
        "ic_smartphone", "ic_tablet", "ic_laptop", "ic_desktop", "ic_watch",
        "ic_tv", "ic_speaker", "ic_headset", "ic_battery_full", "ic_battery_alert",
        "ic_signal_cellular", "ic_wifi", "ic_bluetooth"
    ],
    "image": [
        "ic_image", "ic_image_outline", "ic_photo", "ic_photo_camera",
        "ic_camera_alt", "ic_collections", "ic_crop", "ic_rotate_left", "ic_rotate_right"
    ],
    "file": [
        "ic_folder", "ic_folder_open", "ic_insert_drive_file", "ic_description",
        "ic_cloud", "ic_cloud_upload", "ic_cloud_download", "ic_cloud_done"
    ],
    "social": [
        "ic_person", "ic_person_outline", "ic_people", "ic_people_outline",
        "ic_group", "ic_group_add", "ic_thumb_up", "ic_thumb_down"
    ],
    "places": [
        "ic_location_on", "ic_location_off", "ic_place", "ic_map",
        "ic_directions", "ic_local_shipping", "ic_flight", "ic_hotel"
    ],
    "toggle": [
        "ic_check_box", "ic_check_box_outline_blank", "ic_radio_button_checked",
        "ic_radio_button_unchecked", "ic_toggle_on", "ic_toggle_off", "ic_star", "ic_star_outline"
    ],
    "time": [
        "ic_access_time", "ic_alarm", "ic_alarm_add", "ic_alarm_on", "ic_alarm_off",
        "ic_schedule", "ic_today", "ic_calendar_today", "ic_date_range", "ic_event"
    ],
    "editor": [
        "ic_format_bold", "ic_format_italic", "ic_format_underlined",
        "ic_format_align_left", "ic_format_align_center", "ic_format_align_right",
        "ic_format_list_bulleted", "ic_format_list_numbered"
    ],
    "commerce": [
        "ic_shopping_cart", "ic_shopping_basket", "ic_payment", "ic_credit_card",
        "ic_receipt", "ic_local_offer", "ic_loyalty", "ic_store"
    ],
    "hardware": [
        "ic_keyboard", "ic_mouse", "ic_power", "ic_power_settings_new",
        "ic_router", "ic_cast", "ic_usb", "ic_memory"
    ]
}

# Sample of searchable icons (actual implementation would have all 1546)
ICONS_SEARCHABLE = {
    "ic_mic": {"category": "media", "keywords": ["microphone", "voice", "audio", "record"]},
    "ic_calendar": {"category": "time", "keywords": ["date", "schedule", "event", "appointment"]},
    "ic_calendar_today": {"category": "time", "keywords": ["today", "current", "date"]},
    "ic_calendar_event": {"category": "time", "keywords": ["event", "meeting", "appointment"]},
    "ic_mail": {"category": "communication", "keywords": ["email", "message", "inbox"]},
    "ic_search": {"category": "action", "keywords": ["find", "lookup", "query"]},
    "ic_home": {"category": "navigation", "keywords": ["house", "main", "start"]},
    "ic_settings": {"category": "action", "keywords": ["config", "preferences", "options"]},
    "ic_person": {"category": "social", "keywords": ["user", "profile", "account"]},
    "ic_shopping_cart": {"category": "commerce", "keywords": ["cart", "basket", "buy", "purchase"]},
    "ic_phone": {"category": "communication", "keywords": ["call", "telephone", "dial"]},
    "ic_location_on": {"category": "places", "keywords": ["map", "pin", "gps", "location"]},
    "ic_favorite": {"category": "action", "keywords": ["heart", "like", "love"]},
    "ic_notifications": {"category": "communication", "keywords": ["bell", "alert", "reminder"]},
    "ic_check": {"category": "action", "keywords": ["checkmark", "done", "success", "complete"]},
    "ic_close": {"category": "action", "keywords": ["x", "exit", "cancel", "dismiss"]},
    "ic_arrow_back": {"category": "navigation", "keywords": ["back", "previous", "return"]},
    "ic_menu": {"category": "navigation", "keywords": ["hamburger", "nav", "navigation"]},
}

# Figma Node References
FIGMA_REFERENCES = {
    "homepage": {
        "name": "AI Assistant Homepage",
        "file_key": "yvWQ7pqZSgFIfO0XrzY1me",
        "node_id": "13157:2011",
        "url": "https://www.figma.com/design/yvWQ7pqZSgFIfO0XrzY1me/Home-Page-V2.0?node-id=13157-2011&m=dev",
        "description": "Default homepage layout (360x800px) with voice assistant"
    },
    "menu": {
        "name": "Hamburger Menu",
        "file_key": "gkZ1yhR3PeuOiExiQD1P5r",
        "node_id": "722-14999",
        "url": "https://www.figma.com/design/gkZ1yhR3PeuOiExiQD1P5r/Exploration-new-design?node-id=722-14999&m=dev",
        "description": "Navigation menu structure"
    },
    "chat_page": {
        "name": "Chat Page",
        "file_key": "gkZ1yhR3PeuOiExiQD1P5r",
        "node_id": "718-7049",
        "url": "https://www.figma.com/design/gkZ1yhR3PeuOiExiQD1P5r/Exploration-new-design?node-id=718-7049&m=dev",
        "description": "Chat interface design"
    },
    "media_page": {
        "name": "Media Page",
        "file_key": "gkZ1yhR3PeuOiExiQD1P5r",
        "node_id": "744-4182",
        "url": "https://www.figma.com/design/gkZ1yhR3PeuOiExiQD1P5r/Exploration-new-design?node-id=744-4182&m=dev",
        "description": "Media gallery and player"
    },
    "assistants_page": {
        "name": "Assistants Page",
        "file_key": "gkZ1yhR3PeuOiExiQD1P5r",
        "node_id": "718-7775",
        "url": "https://www.figma.com/design/gkZ1yhR3PeuOiExiQD1P5r/Exploration-new-design?node-id=718-7775&m=dev",
        "description": "AI assistants showcase"
    },
    "tools_page": {
        "name": "Tools Page",
        "file_key": "gkZ1yhR3PeuOiExiQD1P5r",
        "node_id": "720-4552",
        "url": "https://www.figma.com/design/gkZ1yhR3PeuOiExiQD1P5r/Exploration-new-design?node-id=720-4552&m=dev",
        "description": "Tools and utilities page"
    },
    "oneui_design_kit": {
        "name": "OneUI Design Kit (BETA)",
        "file_key": "A1kqKEXc8srjVxPVyFNsQq",
        "url": "https://www.figma.com/design/A1kqKEXc8srjVxPVyFNsQq/OneUI-Design-Kit--BETA-",
        "description": "Updated component specifications"
    },
    "jio_testlab": {
        "name": "Jio Testlab Library",
        "file_key": "W3i7cLkwFbcd8YjDpbRPkT",
        "url": "https://www.figma.com/design/W3i7cLkwFbcd8YjDpbRPkT/Jio-Testlab-Library",
        "description": "Component test boards and specs"
    },
    "chat_input": {
        "name": "Chat Input",
        "file_key": "b95Apii4f27AoRxhm0nJZq",
        "node_id": "19931-32838",
        "url": "https://www.figma.com/design/b95Apii4f27AoRxhm0nJZq/Chat-Input?node-id=19931-32838&m=dev",
        "description": "Chat input states and interactions"
    }
}
