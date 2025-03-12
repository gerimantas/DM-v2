"""
Pre-built templates for common data processing tasks.
These templates can be customized based on user requirements.
"""

# Template for basic CSV data processing
CSV_PROCESSING_TEMPLATE = """
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def process_csv_data(file_path, output_path=None):
    \"\"\"
    Process data from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file
        output_path (str, optional): Path to save processed results
        
    Returns:
        pd.DataFrame: Processed data
    \"\"\"
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Display basic information
    print(f"Data shape: {df.shape}")
    print("\\nData sample:")
    print(df.head())
    
    # Basic data cleaning
    # 1. Remove duplicate rows
    df = df.drop_duplicates()
    
    # 2. Handle missing values
    df = df.dropna()  # Or df.fillna(value) to fill with a specific value
    
    # 3. Basic statistics
    print("\\nBasic statistics:")
    print(df.describe())
    
    # Save processed data if output path is provided
    if output_path:
        df.to_csv(output_path, index=False)
        print(f"\\nProcessed data saved to {output_path}")
    
    return df

# Example usage
if __name__ == "__main__":
    # Replace with your file path
    csv_file = "data.csv"
    processed_data = process_csv_data(csv_file, "processed_data.csv")
"""

# Template for JSON data processing
JSON_PROCESSING_TEMPLATE = """
import json
import pandas as pd
from pathlib import Path

def process_json_data(file_path, output_path=None, flatten=False):
    \"\"\"
    Process data from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file
        output_path (str, optional): Path to save processed results
        flatten (bool): Whether to flatten nested JSON structures
        
    Returns:
        dict or pd.DataFrame: Processed data
    \"\"\"
    # Read the JSON file
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Loaded JSON data from {file_path}")
    
    # Convert to DataFrame if data is a list of records
    if isinstance(data, list):
        df = pd.json_normalize(data) if flatten else pd.DataFrame(data)
        
        # Display basic information
        print(f"\\nData shape: {df.shape}")
        print("\\nData sample:")
        print(df.head())
        
        # Save processed data if output path is provided
        if output_path:
            df.to_csv(output_path, index=False)
            print(f"\\nProcessed data saved to {output_path}")
        
        return df
    else:
        # Handle nested dictionary case
        if flatten and isinstance(data, dict):
            # Attempt to flatten the JSON structure
            flattened = {}
            def flatten_dict(d, parent_key=''):
                for k, v in d.items():
                    key = f"{parent_key}.{k}" if parent_key else k
                    if isinstance(v, dict):
                        flatten_dict(v, key)
                    else:
                        flattened[key] = v
            
            flatten_dict(data)
            data = flattened
        
        # Save processed data if output path is provided
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            print(f"\\nProcessed data saved to {output_path}")
        
        return data

# Example usage
if __name__ == "__main__":
    # Replace with your file path
    json_file = "data.json"
    processed_data = process_json_data(json_file, "processed_data.csv", flatten=True)
"""

# Template for Excel data processing
EXCEL_PROCESSING_TEMPLATE = """
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def process_excel_data(file_path, sheet_name=0, output_path=None):
    \"\"\"
    Process data from an Excel file.
    
    Args:
        file_path (str): Path to the Excel file
        sheet_name (str or int): Sheet to read (name or index)
        output_path (str, optional): Path to save processed results
        
    Returns:
        pd.DataFrame: Processed data
    \"\"\"
    # Read the Excel file
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # Display basic information
    print(f"Data shape: {df.shape}")
    print("\\nData sample:")
    print(df.head())
    
    # Basic data cleaning
    # 1. Remove duplicate rows
    df = df.drop_duplicates()
    
    # 2. Handle missing values
    df = df.dropna()  # Or df.fillna(value) to fill with a specific value
    
    # 3. Basic statistics
    print("\\nBasic statistics:")
    print(df.describe())
    
    # Save processed data if output path is provided
    if output_path:
        # Determine file type from output path
        if output_path.endswith('.csv'):
            df.to_csv(output_path, index=False)
        elif output_path.endswith('.xlsx') or output_path.endswith('.xls'):
            df.to_excel(output_path, index=False)
        else:
            df.to_csv(output_path, index=False)  # Default to CSV
            
        print(f"\\nProcessed data saved to {output_path}")
    
    return df

# Example usage
if __name__ == "__main__":
    # Replace with your file path
    excel_file = "data.xlsx"
    processed_data = process_excel_data(excel_file, sheet_name="Sheet1", output_path="processed_data.csv")
"""

# Template for data visualization
DATA_VISUALIZATION_TEMPLATE = """
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def visualize_data(data, output_dir=None):
    \"\"\"
    Create common visualizations for a dataset.
    
    Args:
        data (pd.DataFrame or str): DataFrame or path to data file (.csv, .xlsx)
        output_dir (str, optional): Directory to save visualizations
        
    Returns:
        None
    \"\"\"
    # Load data if string path is provided
    if isinstance(data, str):
        file_path = Path(data)
        if file_path.suffix.lower() == '.csv':
            df = pd.read_csv(file_path)
        elif file_path.suffix.lower() in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
    else:
        df = data
    
    # Set style
    sns.set(style="whitegrid")
    
    # Create output directory if provided and doesn't exist
    if output_dir:
        out_dir = Path(output_dir)
        out_dir.mkdir(exist_ok=True, parents=True)
    
    # 1. Histogram for each numerical column
    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
    
    for col in numerical_cols:
        plt.figure(figsize=(10, 6))
        sns.histplot(df[col], kde=True)
        plt.title(f'Distribution of {col}')
        plt.tight_layout()
        
        if output_dir:
            plt.savefig(out_dir / f"histogram_{col}.png")
            plt.close()
        else:
            plt.show()
    
    # 2. Count plot for categorical columns
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    
    for col in categorical_cols:
        # Skip columns with too many unique values
        if df[col].nunique() > 10:
            continue
            
        plt.figure(figsize=(10, 6))
        sns.countplot(y=col, data=df, order=df[col].value_counts().index)
        plt.title(f'Count of {col}')
        plt.tight_layout()
        
        if output_dir:
            plt.savefig(out_dir / f"countplot_{col}.png")
            plt.close()
        else:
            plt.show()
    
    # 3. Correlation heatmap for numerical columns
    if len(numerical_cols) > 1:
        plt.figure(figsize=(12, 10))
        correlation = df[numerical_cols].corr()
        sns.heatmap(correlation, annot=True, cmap='coolwarm', linewidths=0.5)
        plt.title('Correlation Heatmap')
        plt.tight_layout()
        
        if output_dir:
            plt.savefig(out_dir / "correlation_heatmap.png")
            plt.close()
        else:
            plt.show()
    
    # 4. Pair plot for numerical columns (limited to 5 columns max for readability)
    if len(numerical_cols) > 1:
        plot_cols = numerical_cols[:min(5, len(numerical_cols))]
        plt.figure(figsize=(15, 15))
        sns.pairplot(df[plot_cols])
        plt.suptitle('Pair Plot of Numerical Features', y=1.02)
        
        if output_dir:
            plt.savefig(out_dir / "pair_plot.png")
            plt.close()
        else:
            plt.show()
    
    print("Visualization complete!")

# Example usage
if __name__ == "__main__":
    # Replace with your data file path
    data_file = "data.csv"
    visualize_data(data_file, "visualizations")
"""

# Dictionary mapping template names to their content
TEMPLATES = {
    "csv_processing": CSV_PROCESSING_TEMPLATE,
    "json_processing": JSON_PROCESSING_TEMPLATE,
    "excel_processing": EXCEL_PROCESSING_TEMPLATE,
    "data_visualization": DATA_VISUALIZATION_TEMPLATE
}

def get_template(template_name):
    """
    Get a template by name.
    
    Args:
        template_name (str): Name of the template
        
    Returns:
        str: Template content
    """
    return TEMPLATES.get(template_name, "Template not found")

def list_templates():
    """
    List all available templates.
    
    Returns:
        list: Names of available templates
    """
    return list(TEMPLATES.keys())