import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from doc_distill.converter import PDFConverter
from doc_distill.compressor import PromptCompressor

app = typer.Typer(help="Convert PDFs to Markdown and optionally compress them for LLMs.")
console = Console()

@app.callback()
def main():
    """
    Doc-Distill CLI tool.
    """
    pass

@app.command()
def convert(
    path: Path = typer.Argument(..., help="Path to a PDF file or a directory of PDFs."),
    ocr: bool = typer.Option(False, "--ocr", help="Enable OCR for scanned documents (requires Tesseract)."),
    compress: bool = typer.Option(False, "--compress", "-c", help="Generate a compressed version for LLMs."),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Custom output directory. Defaults to source directory.")
):
    """
    Convert PDF(s) to Markdown.

    This command processes a single PDF file or a directory of PDF files.
    It converts the content to Markdown format and optionally creates a compressed
    version optimized for Large Language Models (LLMs).

    Args:
        path (Path): The file path to a single PDF or a directory containing PDFs.
        ocr (bool): If True, enables Optical Character Recognition (OCR) for scanned documents.
                    Requires Tesseract to be installed. Defaults to False.
        compress (bool): If True, generates an additional compressed Markdown file
                         with stop words and punctuation removed. Defaults to False.
        output (Optional[Path]): The directory where output files will be saved.
                                 If not provided, files are saved in the same directory as the source.
    """
    
    # Validate Inputs
    if not path.exists():
        console.print(f"[red]Error: Path '{path}' does not exist.[/red]")
        raise typer.Exit(code=1)

    files_to_process = []
    if path.is_file():
        if path.suffix.lower() == ".pdf":
            files_to_process.append(path)
        else:
            console.print("[red]Error: File is not a PDF.[/red]")
            raise typer.Exit(code=1)
    elif path.is_dir():
        files_to_process = list(path.glob("*.pdf"))
        if not files_to_process:
            console.print(f"[yellow]No PDFs found in directory '{path}'.[/yellow]")
            raise typer.Exit()

    # Initialize Tools
    converter = PDFConverter(ocr_enabled=ocr)
    compressor = PromptCompressor() if compress else None

    # Processing Loop
    for pdf_file in files_to_process:
        console.print(f"Processing [bold cyan]{pdf_file.name}[/bold cyan]...")
        
        try:
            # 1. Convert
            md_content = converter.to_markdown(str(pdf_file))
            
            # Determine Output Path
            out_dir = output if output else pdf_file.parent
            if not out_dir.exists():
                out_dir.mkdir(parents=True, exist_ok=True)

            # 2. Save Regular Markdown
            base_name = pdf_file.stem
            md_path = out_dir / f"{base_name}.md"
            
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(md_content)
            console.print(f"  [green]Saved:[/green] {md_path}")

            # 3. Compress (Optional)
            if compress and compressor:
                compressed_content = compressor.compress(md_content)
                
                # Append naming convention per requirements
                comp_path = out_dir / f"{base_name}_compressed.md"
                with open(comp_path, "w", encoding="utf-8") as f:
                    f.write(compressed_content)
                console.print(f"  [green]Compressed:[/green] {comp_path}")

        except Exception as e:
            console.print(f"  [red]Failed to process {pdf_file.name}: {e}[/red]")

if __name__ == "__main__":
    app()