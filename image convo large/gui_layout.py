import wx
import image_utils # To access the OUTPUT_FORMATS list

def initial_summary_text():
    return "Batch Summary:\nOriginal Total: 0.00 KB\nCompressed Total: 0.00 KB\nTotal Savings: 0.00 KB (0.0%)"

def build_ui(frame, panel):
    """
    Constructs all UI elements and assigns them to the frame object.
    """
    panel.SetBackgroundColour("#93B7DB")
    main_sizer = wx.BoxSizer(wx.VERTICAL)

    # --- Header ---
    title = wx.StaticText(panel, label="Python Image Processing Mini Project")
    title_font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
    title.SetFont(title_font)
    title.SetForegroundColour("#0A1F44")
    main_sizer.Add(title, 0, wx.ALIGN_CENTER | wx.ALL, 15)

    # Select images
    frame.select_btn = wx.Button(panel, label="Select Images (Batch)")
    main_sizer.Add(frame.select_btn, 0, wx.ALL | wx.EXPAND, 8)

    frame.paths_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(-1, 50))
    frame.paths_text.SetValue("No image selected")
    main_sizer.Add(frame.paths_text, 0, wx.ALL | wx.EXPAND, 8)

    # Options area
    grid = wx.FlexGridSizer(cols=2, hgap=10, vgap=10)
    grid.AddGrowableCol(1, 1)

    # Output Format
    grid.Add(wx.StaticText(panel, label="Output Format:"), 0, wx.ALIGN_CENTER_VERTICAL)
    frame.format_choice = wx.ComboBox(panel, choices=image_utils.OUTPUT_FORMATS, style=wx.CB_READONLY)
    frame.format_choice.SetSelection(0)
    grid.Add(frame.format_choice, 1, wx.EXPAND)

    # Quality Slider
    grid.Add(wx.StaticText(panel, label="Quality (1-100):"), 0, wx.ALIGN_CENTER_VERTICAL)
    frame.quality_slider = wx.Slider(panel, minValue=1, maxValue=100, value=80, style=wx.SL_HORIZONTAL)
    grid.Add(frame.quality_slider, 1, wx.EXPAND)

    # Grayscale Checkbox
    grid.Add(wx.StaticText(panel, label="Grayscale:"), 0, wx.ALIGN_CENTER_VERTICAL)
    frame.gray_checkbox = wx.CheckBox(panel, label="Convert to Grayscale")
    grid.Add(frame.gray_checkbox, 1, wx.EXPAND)

    main_sizer.Add(grid, 0, wx.ALL | wx.EXPAND, 8)

    # Target size
    hbox_target = wx.BoxSizer(wx.HORIZONTAL)
    frame.target_checkbox = wx.CheckBox(panel, label="Enable Target File Size (KB):")
    hbox_target.Add(frame.target_checkbox, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 8)
    frame.target_input = wx.TextCtrl(panel)
    frame.target_input.SetHint("e.g., 50")
    hbox_target.Add(frame.target_input, 1, wx.EXPAND)
    main_sizer.Add(hbox_target, 0, wx.ALL | wx.EXPAND, 8)

    # Start button
    frame.start_btn = wx.Button(panel, label="Start Batch Conversion")
    main_sizer.Add(frame.start_btn, 0, wx.ALL | wx.EXPAND, 12)

    # Status & progress
    frame.status_label = wx.StaticText(panel, label="")
    main_sizer.Add(frame.status_label, 0, wx.ALL, 6)

    frame.progress = wx.Gauge(panel, range=100, style=wx.GA_HORIZONTAL)
    main_sizer.Add(frame.progress, 0, wx.ALL | wx.EXPAND, 6)

    # Comparison summary
    frame.summary_text = wx.StaticText(panel, label=initial_summary_text())
    main_sizer.Add(frame.summary_text, 0, wx.ALL | wx.EXPAND, 6)

    panel.SetSizer(main_sizer)