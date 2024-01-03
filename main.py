import csv
from jinja2 import Environment, FileSystemLoader
import os
import webbrowser  # Import the webbrowser module


def generate_html_batch(csv_filename, output_directory, dated, outletName, closeDate, branch, batch_size=30, title='Bulk Letter'):
    # Load Jinja2 environment and template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template.html')

    # Read CSV data
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        rows = list(csv_reader)

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Generate HTML in batches
    for batch_number in range(0, len(rows), batch_size):
        batch_rows = rows[batch_number:batch_number + batch_size]
        combined_html = ""
        batch_count = 0  # Reset count for each batch

        for row in batch_rows:
            try:
                batch_count += 1  # Increment the batch count
                count = batch_number + batch_count  # Calculate row count

                output_html = template.render(
                    ref=f'SBL/ABD/2024/100{count}',
                    date=dated,
                    outletName=outletName,
                    closeDate=closeDate,
                    branch=branch,
                    title=title,
                    account_title=row['AccountTitel'],
                    address=row['Address'],
                    contact=row['Contact'],
                    masked_account_no=row['AccountNo'][:5] +
                    '***' + row['AccountNo'][8:],
                )

                # Concatenate the HTML for each row
                print(f"Generating HTML for row {count} Batch {
                      batch_number // batch_size + 1}")
                combined_html += output_html
            except Exception as e:
                print(f"Error processing row {count}: {e}")

        # Save the combined HTML for the batch
        batch_output_file = os.path.join(output_directory, f"batch_{
                                         batch_number // batch_size + 1}.html")
        try:
            with open(batch_output_file, 'w', encoding='utf-8') as html_file:
                html_file.write(combined_html)
            print(f'Batch HTML file "{
                  batch_output_file}" generated successfully.')

            # Open the HTML file in a web browser
            webbrowser.open_new_tab(batch_output_file)
        except Exception as e:
            print(f"Error saving HTML file for batch {
                  batch_number // batch_size + 1}: {e}")


if __name__ == '__main__':
    csv_filename = "list.csv"
    output_directory = "output"
    dated = "৩রা জানুয়ারী, ২০২৪"
    outletName = "কার্পাসডাঙ্গা বাজার"
    closeDate = "১৮ই জানুয়ারী ২০২৪"
    branch = "চুয়াডাঙ্গা শাখা "
    generate_html_batch(csv_filename, output_directory,
                        dated, outletName, closeDate, branch)
