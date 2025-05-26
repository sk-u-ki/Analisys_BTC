def main():
    from data_processing.csv_handler import load_and_process_data
    from html_generation.index_page import generate_index_page
    from utils.helpers import setup_logging

    # Setup logging
    setup_logging()

    # Load and process data
    data = load_and_process_data('data/input_data.csv')

    # Generate HTML index page
    generate_index_page(data)

if __name__ == "__main__":
    main()