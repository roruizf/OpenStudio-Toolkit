import logging
import os
import re

import pandas as pd

# Configure logger
logger = logging.getLogger(__name__)

def extract_table_by_name_from_energyplus_results_html(html_file_path: str, table_name: str) -> pd.DataFrame | None:
    """
    Extract a specific table from an EnergyPlus results HTML file based on its title.

    This function searches for the specified table name enclosed in <b> tags and parses 
    the immediately following <table> element into a pandas DataFrame.

    Parameters:
    - html_file_path (str): Path to the EnergyPlus 'eplusout.htm' file.
    - table_name (str): The exact text name of the table (e.g., 'Zone Sensible Cooling').

    Returns:
    - Optional[pd.DataFrame]: The extracted table as a DataFrame, or None if not found or parsing fails.
    """
    table_label = f'<b>{table_name}</b>'

    try:
        if not os.path.exists(html_file_path):
            logger.error(f"EnergyPlus HTML file not found: {html_file_path}")
            return None
            
        with open(html_file_path, encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        logger.error(f"Error reading HTML file: {str(e)}")
        return None

    # Locate the table label
    start_index = html_content.find(table_label)
    if start_index == -1:
        logger.warning(f"Table title '{table_name}' not found in HTML.")
        return None
        
    start_index += len(table_label)
    start_index = html_content.find('<table', start_index)
    if start_index == -1:
        logger.warning(f"No table element found following title '{table_name}'.")
        return None

    # Locate the end of the table
    end_index = html_content.find('</table>', start_index)
    if end_index == -1:
        logger.error(f"Closing </table> tag missing for table '{table_name}'.")
        return None

    table_html = html_content[start_index:end_index + len('</table>')]

    # Extract rows using regex
    rows = re.findall(r'<tr.*?>(.*?)</tr>', table_html, re.DOTALL)
    if not rows:
        logger.warning(f"No rows found in table '{table_name}'.")
        return None

    data = []
    headers = []
    for i, row_html in enumerate(rows):
        # Extract cells (th or td)
        cells = re.findall(r'<(th|td).*?>(.*?)</\1>', row_html, re.DOTALL)
        row_values = [cell[1].strip() for cell in cells]
        
        if i == 0:
            headers = row_values
        elif row_values:
            data.append(row_values)

    if not data:
        logger.warning(f"Table '{table_name}' contains no data rows.")
        return None

    df = pd.DataFrame(data, columns=headers if headers else None)
    logger.info(f"Successfully extracted table '{table_name}' with {len(df)} rows.")
    return df