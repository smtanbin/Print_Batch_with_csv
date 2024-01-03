import os
import csv
from jinja2 import Environment, FileSystemLoader

def generate_html(csv_filename, html_output_file, dated, outletName, closeDate, branch, title='CSV to HTML'):
    # Load Jinja2 environment and template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template.html')

    # Read CSV data
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        rows = list(csv_reader)

    # Render the template for each row
    combined_html = ""
    for row in rows:
        output_html = template.render(
            date=dated,
            outletName=outletName,
            closeDate=closeDate,
            branch=branch,
            title=title,
            account_title=row['AccountTitel'],
            address=row['Address'],
            contact=row['Contact'],
            masked_account_no=row['AccountNo'][:5] + '***' + row['AccountNo'][8:],
        )

        # Concatenate the HTML for each row
        combined_html += output_html

    # Save the combined HTML
    with open(html_output_file, 'w', encoding='utf-8') as html_file:
        html_file.write(combined_html)

if __name__ == '__main__':
    csv_filename = "list.csv"
    html_output_file = "output/combined_output.html"

    dated = "৩রা জানুয়ারী, ২০২৪"
    outletName = "কার্পাসডাঙ্গা বাজার"
    closeDate = "১৮ই জানুয়ারী ২০২৪"
    branch = "চুয়াডাঙ্গা শাখা "

    generate_html(csv_filename, html_output_file,dated,outletName,closeDate,branch)
    print(f'Combined HTML file "{html_output_file}" generated successfully.')
