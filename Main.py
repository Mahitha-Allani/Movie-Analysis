from modules.data_loader import load_data
from modules.plots import show_data_info, plot_ratings, plot_genres, show_top_movies_grading,  plot_single_movie_review_paginated
import os
#from modules.utils import split_genres
def main():
    print("=== MovieLens Data Analysis ===\n")

    datasets_folder = os.path.join(os.path.dirname(__file__), "datasets")
    
    if not load_data(datasets_folder):
        print("Error: Could not load datasets from 'datasets/' folder!")
        return
   # main menu
    while True:
        print("\nSelect an option:")
        print("1 - Show dataset info")
        print("2 - Show ratings distribution graph")
        print("3 - Show genre distribution graph")
        print("4 - Show top movies review graph")
        print("5 - Show individual movie review graph")
        print("0 - Exit")
        #try to get user input
        try:
             choice = input("Enter your choice: ").strip()
        except EOFError:
                print("\nInput not available. Exiting...")
                break

        #check user input
        if choice == '1':
            show_data_info()
        elif choice == '2':
            plot_ratings()
        elif choice == '3':
            plot_genres()
        elif choice == '4':
             top_n = input("How many top movies to show in grading table? (default 10): ").strip()
             top_n = int(top_n) if top_n.isdigit() else 10
             show_top_movies_grading(top_n=top_n)

        elif choice == '5':
          plot_single_movie_review_paginated()

        elif choice == '0':
            print("Exiting program.")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
