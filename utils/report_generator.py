import json
import os
from pathlib import Path

class ReportGenerator:
    """Handles the generation and storage of reports in various formats."""
    
    def __init__(self, target: str):
        self.target = target
        self.report_dir = Path("reports") / target
        self.report_dir.mkdir(parents=True, exist_ok=True)

        # Find the next available run number
        self.run_number = 1
        while (self.report_dir / f"Run{self.run_number}").exists():
            self.run_number += 1
        
        # Create the new run directory
        self.run_dir = self.report_dir / f"Run{self.run_number}"
        self.run_dir.mkdir(parents=True, exist_ok=True)

    def generate_html(self, results):
        """Generate an HTML report from a dictionary of results."""
        html_content = f"""
        <html>
        <head>
            <title>ZeroSight Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                h1, h2, h3 {{ color: #333; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ padding: 8px 12px; border: 1px solid #ccc; }}
                th {{ background-color: #f2f2f2; }}
                .success {{ color: green; }}
                .failed {{ color: red; }}
                .timeout {{ color: orange; }}
            </style>
        </head>
        <body>
            <h1>ZeroSight Report</h1>
            <h2>Target: {self.target}</h2>
            <h3>Run Number: {self.run_number}</h3>
            <table>
                <tr><th>Tool</th><th>Status</th><th>Output</th><th>Error</th></tr>
        """
        
        for result in results:
            status_class = result['status']
            html_content += f"""
                <tr>
                    <td>{result['tool']}</td>
                    <td class='{status_class}'>{result['status']}</td>
                    <td><pre>{result.get('output', '')}</pre></td>
                    <td><pre>{result.get('error', '')}</pre></td>
                </tr>
            """

        html_content += """
            </table>
        </body>
        </html>
        """

        with open(self.run_dir / 'report.html', 'w') as f:
            f.write(html_content)

    def generate_txt(self, results):
        """Generate a plain text report from results."""
        txt_content = []
        txt_content.append(f"ZeroSight Report - Target: {self.target}\n")
        txt_content.append(f"Run Number: {self.run_number}\n")
        txt_content.append("=" * 80 + "\n")

        for result in results:
            txt_content.append(f"Tool: {result['tool']}")
            txt_content.append(f"Status: {result['status']}")
            txt_content.append(f"Output:\n{result.get('output', '')}\n")
            txt_content.append(f"Error:\n{result.get('error', '')}\n")
            txt_content.append("=" * 80 + "\n")

        with open(self.run_dir / 'report.txt', 'w') as f:
            f.writelines(txt_content)

    def generate_json(self, results):
        """Generate a JSON report."""
        with open(self.run_dir / 'report.json', 'w') as f:
            json.dump(results, f, indent=4)

    def save_report(self, results):
        """Save all report formats."""
        self.generate_html(results)
        self.generate_txt(results)
        self.generate_json(results)

