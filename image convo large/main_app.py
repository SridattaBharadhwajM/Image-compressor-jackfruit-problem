import wx
import os
from PIL import Image
# Member 1's File (Backend Core)
import image_utils       
# Member 2's File (Compression Algorithm)
import compression_logic 
# Member 3's File (UI Design/Layout - using the original name)
import gui_layout       
class ImageConverterFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Multi-Format Image Converter", size=(760, 600))
        self.selected_paths = []
        # 1. Initialize UI using Member 3's module
        panel = wx.Panel(self)
        gui_layout.build_ui(self, panel)
        # 2. Bind Events
        self.select_btn.Bind(wx.EVT_BUTTON, self.on_select_images)
        self.start_btn.Bind(wx.EVT_BUTTON, self.on_start_conversion)
        self.quality_slider.Bind(wx.EVT_SLIDER, self.on_quality_change)
        self.Centre()
        self.Show()
    def update_status(self, text, color=wx.Colour(0, 120, 0)):
        self.status_label.SetLabel(text)
        try:
            self.status_label.SetForegroundColour(color)
        except Exception:
            pass
    def update_summary(self, original_size_bytes, final_size_bytes):
        if original_size_bytes == 0:
            self.summary_text.SetLabel(gui_layout.initial_summary_text()) # Correct call
            return
        original_kb = original_size_bytes / 1024
        final_kb = final_size_bytes / 1024
        savings = max(0, original_kb - final_kb)
        percentage = (savings / original_kb) * 100 if original_kb > 0 else 0
        comparison_text = (f"Batch Summary:\n" f"Original Total: {original_kb:,.2f} KB\n" f"Compressed Total: {final_kb:,.2f} KB\n" f"Total Savings: {savings:,.2f} KB ({percentage:.1f}%)")
        self.summary_text.SetLabel(comparison_text)
    #  Event Handlers (Controller) 
    def on_select_images(self, event):
        wildcard = "Image files (*.jpeg;*.jpg;*.png;*.gif;*.tiff;*.tif;*.bmp;*.webp)|*.jpeg;*.jpg;*.png;*.gif;*.tiff;*.tif;*.bmp;*.webp"
        dlg = wx.FileDialog(self, "Select images", wildcard=wildcard,
                            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.selected_paths = dlg.GetPaths()
            self.paths_text.SetValue("\n".join(self.selected_paths))
            self.update_status(f"{len(self.selected_paths)} images selected for processing.")
            self.summary_text.SetLabel(gui_layout.initial_summary_text()) # Correct call
        dlg.Destroy()
    def on_quality_change(self, event):
        val = self.quality_slider.GetValue()
        self.quality_slider.SetToolTip(wx.ToolTip(f"Quality: {val}"))
    def on_start_conversion(self, event):
        if not self.selected_paths:
            wx.MessageBox("Please select images first.", "No images", wx.OK | wx.ICON_WARNING)
            return
        # Gather settings
        to_grayscale = self.gray_checkbox.IsChecked()
        use_target_size = self.target_checkbox.IsChecked()
        quality = int(self.quality_slider.GetValue())
        target_size_kb = 0
        if use_target_size:
            try:
                target_size_kb = int(self.target_input.GetValue().strip())
                if target_size_kb <= 0: raise ValueError
            except Exception:
                wx.MessageBox("Enter a valid positive number for target size (KB).", "Invalid input", wx.OK | wx.ICON_ERROR)
                return
        output_format_pil = image_utils.format_to_pil_ext(self.format_choice.GetValue())
        # Ask for output directory
        dlg = wx.DirDialog(self, "Select Output Directory", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() != wx.ID_OK: return
        output_dir = dlg.GetPath()
        dlg.Destroy()
        # Start the batch process
        self.process_batch(self.selected_paths, output_dir, output_format_pil,
                           quality, to_grayscale, use_target_size, target_size_kb)
    def process_batch(self, input_paths, output_dir, output_format_pil, quality, to_grayscale, use_target_size, target_size_kb):
        processed_count = 0
        total_files = len(input_paths)
        total_original_size_bytes = 0
        total_compressed_size_bytes = 0
        self.progress.SetRange(total_files if total_files > 0 else 1)
        self.progress.SetValue(0)
        for idx, input_path in enumerate(input_paths, start=1):
            try:
                # 1. Image Utility (Member 1)
                original_file_size = os.path.getsize(input_path)
                total_original_size_bytes += original_file_size
                image = image_utils.open_image_simple(input_path)
                if image is None: continue 
                # 2. Grayscale conversion
                if to_grayscale:
                    image = image.convert('L')
                # 3. Compression Logic (Member 2)
                final_quality = quality
                if use_target_size:
                    # Calls the logic from the compression_logic module
                    final_quality = compression_logic.compress_to_target_size(image.copy(), target_size_kb, output_format_pil)
                # 4. file
                original_filename = os.path.basename(input_path)
                base, _ = os.path.splitext(original_filename)
                out_ext = output_format_pil.lower() if output_format_pil.lower() != "jpeg" else "jpg"
                output_path = os.path.join(output_dir, f"{base}.{out_ext}")
                # Calls the save function from the image_utils module
                image_utils.save_image_processed(image, output_path, output_format_pil, final_quality)
                compressed_file_size = os.path.getsize(output_path)
                total_compressed_size_bytes += compressed_file_size
                processed_count += 1
                # Update status
                self.update_status(f"Processing {processed_count}/{total_files}: {os.path.basename(input_path)}")
                self.progress.SetValue(idx)
                wx.YieldIfNeeded()
            except Exception as e:
                # Print to console for debugging and continue to the next file
                print(f"Error processing {input_path}: {e}")
        self.update_status(f"Batch processing complete! {processed_count} files saved to {output_dir}")
        self.update_summary(total_original_size_bytes, total_compressed_size_bytes)
if __name__ == "__main__":
    app = wx.App(False)
    frame = ImageConverterFrame()
    app.MainLoop()
