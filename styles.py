# ========================
# styles.py – AI INTERVIEW X
# Premium Design System
# ========================

class AppTheme:
    """
    Elegant, modern & professional design system
    Optimized for interview platforms and AI tools
    """

    # -------------------------------------------------
    # Core Brand Colors (Refined)
    # -------------------------------------------------

    PRIMARY_DARK = "#0B1E33"       # Rich deep navy (more premium)
    ACCENT_ORANGE = "#F39C5A"     # Softer luxury orange
    BG_LIGHT = "#F2F4F7"          # Clean neutral background

    # -------------------------------------------------
    # Neutral Palette
    # -------------------------------------------------

    WHITE = "#FFFFFF"
    TEXT_DARK = "#1C1C1E"         # iOS-like rich dark text
    TEXT_LIGHT = "#6E6E73"        # Secondary text
    BORDER_SUBTLE = "#E0E0E5"     # Very light border
    DIVIDER = "#E8E8ED"

    # -------------------------------------------------
    # Feedback Colors
    # -------------------------------------------------

    SUCCESS_GREEN = "#27AE60"
    WARNING_RED = "#E74C3C"
    INFO_BLUE = "#3498DB"
    NEUTRAL_GRAY = "#9B9B9B"

    # -------------------------------------------------
    # Shadows & Elevation
    # -------------------------------------------------

    SHADOW_COLOR_LIGHT = "#00000012"   # Very soft shadow
    SHADOW_COLOR_MEDIUM = "#00000025"
    SHADOW_COLOR_DEEP = "#00000040"

    # -------------------------------------------------
    # Typography
    # -------------------------------------------------

    FONT_FAMILY = "Segoe UI"

    FONT_HEADER = (FONT_FAMILY, 18, "bold")
    FONT_SUBHEADER = (FONT_FAMILY, 14, "bold")
    FONT_LABEL = (FONT_FAMILY, 11, "normal")
    FONT_TEXT = (FONT_FAMILY, 11, "normal")
    FONT_SMALL = (FONT_FAMILY, 10, "normal")
    FONT_MONO = ("Consolas", 11, "normal")

    # -------------------------------------------------
    # Spacing Scale (8-point system)
    # -------------------------------------------------

    PADDING_XXS = 2
    PADDING_XS = 6
    PADDING_SM = 10
    PADDING_MD = 14
    PADDING_LG = 18
    PADDING_XL = 24
    PADDING_XXL = 32

    # -------------------------------------------------
    # Borders & Corners
    # -------------------------------------------------

    BORDER_WIDTH_THIN = 1
    BORDER_WIDTH_THICK = 2
    BORDER_RELIEF = "flat"

    # Simulated corner radius sizes
    RADIUS_SM = 6
    RADIUS_MD = 10
    RADIUS_LG = 16

    # -------------------------------------------------
    # Button Styles (Reference Values)
    # -------------------------------------------------

    BTN_PRIMARY_BG = ACCENT_ORANGE
    BTN_PRIMARY_FG = WHITE

    BTN_SECONDARY_BG = PRIMARY_DARK
    BTN_SECONDARY_FG = WHITE

    BTN_DISABLED_BG = "#CFCFCF"
    BTN_DISABLED_FG = "#8A8A8A"

    # -------------------------------------------------
    # Text Field Styles
    # -------------------------------------------------

    INPUT_BG = WHITE
    INPUT_FG = TEXT_DARK
    INPUT_PLACEHOLDER = TEXT_LIGHT
    INPUT_BORDER = BORDER_SUBTLE
    INPUT_ACTIVE_BORDER = ACCENT_ORANGE

    # -------------------------------------------------
    # Status Indicators
    # -------------------------------------------------

    STATUS_SUCCESS_BG = "#EAF8F0"
    STATUS_WARNING_BG = "#FDEDEC"
    STATUS_INFO_BG = "#EBF5FB"

    STATUS_SUCCESS_TEXT = SUCCESS_GREEN
    STATUS_WARNING_TEXT = WARNING_RED
    STATUS_INFO_TEXT = INFO_BLUE
