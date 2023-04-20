#########################################
##### Name:Reema Hamasha            #####
##### Uniqname:hamashar             #####
#########################################

import webbrowser as wb
import requests
import json
import csv
import pandas as pd

#API Setup
class OpenLibraryBooksAPI:
    def __init__(self):
        self.base_url = "https://openlibrary.org/"
        self.api_url = self.base_url + "search.json"
        self.session = requests.Session()



    def search_books(self, query):
        params = {
            "q": query,
            'limit': 1
        }
        response = self.session.get(self.api_url, params=params)
        response_data = response.json()

        # Extract the relevant fields from each book in the search results
        books = response_data["docs"]
        book_info = [{"Title": book.get("title", []),
                    "Author Name": ", ".join(book.get("author_name", [])),
                    "Publisher": book.get("publisher", [])[0],
                    "Publish Year": book.get("publish_year", [])[0], 
                    "Number of Pages": book.get("number_of_pages_median", []),
                    "ISBN": book.get("isbn", [])[0]} 
                    for book in books]

        # Format book_info as a numbered list
        book_list = ""
        for i, book in enumerate(book_info, 1):
            book_list += f"{i}. {book['Title']}\n"
            book_list += f"    Author Name: {book['Author Name']}\n"
            book_list += f"    Publisher: {book['Publisher']}\n"
            book_list += f"    Publish Year: {book['Publish Year']}\n"
            book_list += f"    Number of Pages: {book['Number of Pages']}\n"
            book_list += f"    ISBN: {book['ISBN']}\n\n"

        return book_list

    def title_author(self, query):
        params = {
            "q": query,
            'limit': 1
        }
        response = self.session.get(self.api_url, params=params)
        response_data = response.json()

        # Extract the relevant fields from each book in the search results
        books = response_data["docs"]
        book_info = [{"Title": book.get("title", []),
                    "Author Name": ", ".join(book.get("author_name", [])),
                    "Number of Pages": book.get("number_of_pages_median", [])
                    } 
                    for book in books]

        # Format book_info as a numbered list
        book_list = ""
        for i, book in enumerate(book_info, 1):
            book_list += f"    {book['Title']}\n"
            book_list += f"    Author Name: {book['Author Name']}\n"
            book_list += f"    Number of Pages: {book['Number of Pages']} pages\n\n"
        return book_list


    def top_subjects(self, query):
        params = {
            "q": query,
            'limit': 1
         }
        response = self.session.get(self.api_url, params=params)
        response_data = response.json()
        

        # Extract the publish_year and author_name fields from each book in the search results
        books = response_data["docs"]
        book_info = [{"title": book.get("title", []),
                      "subjects": book.get("subject", [])[:5]}
                     for book in books]

        # Format the list of subjects as a numbered list
        formatted_subjects = []
        for i, book in enumerate(book_info):
            formatted_subjects.append(f"{book['title']}")
            for j, subject in enumerate(book['subjects']):
                formatted_subjects.append(f"    {j + 1}. {subject}")
        result_text = "\n".join(formatted_subjects)

        return result_text
    
    def publishing_info(self, query):
        params = {
            "q": query,
            'limit': 1
        }
        response = self.session.get(self.api_url, params=params)
        response_data = response.json()

        # Extract the relevant fields from each book in the search results
        books = response_data["docs"]
        book_info = [{"Title": book.get("title", []),
                    "Publisher": book.get("publisher", [])[0],
                    "Publish Year": book.get("publish_year", [])[0]
                    }
                    for book in books]

        # Format book_info as a numbered list
        book_list = ""
        for i, book in enumerate(book_info, 1):
            book_list += f"{book['Title']}\n"
            book_list += f"    Publisher: {book['Publisher']}\n"
            book_list += f"    Publish Year: {book['Publish Year']}\n\n"

        return book_list
    

    def get_top_subjects(self, isbn):
            url = f"{self.base_url}/isbn/{isbn}.json"
            response = self.session.get(url)
            response_data = response.json()
            
            # Get the top 5 subjects from the response
            top_subjects = []
            subjects = response_data.get("subjects", [])
            if subjects:
                top_subjects = [subject.get("name") for subject in subjects[:5]]
            
            return top_subjects
    
    def get_title(self, query):
            params = {
                "q": query,
                "limit": 1  # limit to 1 search result
            }
            response = requests.get(self.api_url, params=params)
            response_data = response.json()

            # Extract the book title from the search result
            book = response_data["docs"][0]
            title = book["title"]

            return title



api = OpenLibraryBooksAPI()
book_results = api.search_books("harry potter")
print("BOOK RESULTS")
print(book_results)

title_author_test = api.title_author("harry potter")
print("Title/Author")
print(title_author_test)

top5_subjects_test = api.top_subjects('harry potter')
print("top 5 subjects")
print(top5_subjects_test)

publishing_test = api.publishing_info('harry potter')
print('publishing info')
print(publishing_test)

title_results = api.get_title('hunger games')
print("TITLES")
print(title_results)




# Read in the CSV file
df = pd.read_csv('movies_metadata.csv')
df.dropna(subset=['title'], inplace=True)
# print(df.head())
# View the first 5 rows
# print(df.head())

# for col in df.columns:
#     print(col)

small_df = df[['title','release_date',"budget","imdb_id", 'runtime','overview']]
# print(small_df.head())


# # check if the book title is in the movies metadata
# if df['title'].str.contains(book_title).any():
#     print(f"{book_title} is in the movies metadata!")
# else:
#     print(f"{book_title} is not in the movies metadata.")


# Find rows that contain "Harry Potter"
# book_movie_row = df[df['title'].str.contains(book_title)]

# Print the rows
# print(book_movie_row.iloc[0]['budget'])


class Node:
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)
        
    def set_book_results(self, book_results):
        self.book_results = book_results
        
    def set_publisher_results(self, publisher_results):
        self.publisher_results = publisher_results
        
    def set_subject_results(self, subject_results):
        self.subject_results = subject_results
        
    def set_movie_results(self, movie_results):
        self.movie_results = movie_results


def tree_to_string(node, level=0):
    """Converts the tree to a string representation."""
    # Create a string to represent the node
    node_string = "\t" * level + str(node.data) + "\n"

    # Recursively add the children's string representation to this string
    for child in node.children:
        node_string += tree_to_string(child, level=level+1)

    return node_string


if __name__ == "__main__":
    root_node = Node(None)
    # current_node = root_node
    current_node = root_node

    while True:
        # get user input
        input_term = input("Enter a book title or enter exit to quit: ")

        if input_term.lower() == "exit":
            print("Bye")
            break
        
        # create new node for this input
        # new_node = Node(input_term)
        
        # add child node to current node
        # current_node.add_child(new_node)
        
        # get book results
        book_results = api.title_author(input_term)
        print(book_results)
        book_node = Node(book_results)
        current_node.add_child(book_node)
        
        # ask about publishing info
        publishing_choice = input(f"Would you like to learn the about the publishing information? Yes or No? ")
        if publishing_choice.lower() == "yes":
            publisher_results = api.publishing_info(input_term)
            print(publisher_results)
            publish_node = Node(publisher_results)
            current_node.add_child(publish_node)
        
        # ask about top subjects
        subjects_choice = input(f"Would you like to learn the about the top 5 subjects in this book? Yes or No? ")
        if subjects_choice.lower() == "yes":
            subject_results = api.top_subjects(input_term)
            print(subject_results)
            subjects_node = Node(subject_results)
            current_node.add_child(subjects_node)
        
        # ask about movie adaptation
        movies_choice = input(f"Would you like to know if this book has been turned into a movie? Yes or No? ")
        if movies_choice.lower() == "yes":
            book_title = api.get_title(input_term)
            if df['title'].str.contains(book_title).any():
                # print(f"{book_title} is in the movies metadata!")
                movie_results = small_df[small_df['title'].str.contains(book_title)].iloc[0]
                print(f"Title: {movie_results['title']}")
                print(f"Release Date: {movie_results['release_date']}")
                print(f"Budget: ${movie_results['budget']}")
                print(f"IMDB ID: {movie_results['imdb_id']}")
                print(f"Runtime: {movie_results['runtime']} minutes")
                print(f"Overview: {movie_results['overview']}")
                movie_node = Node(f"\nTitle: {movie_results['title']}\nRelease Date: {movie_results['release_date']}\nBudget: ${movie_results['budget']}\nIMDB ID: {movie_results['imdb_id']}\nRuntime: {movie_results['runtime']} minutes\nOverview: {movie_results['overview']}")
                current_node.add_child(movie_node)
            else:
                print(f"{book_title} is not in the movies metadata.")

        
        # update current node to be the new node
        # current_node = new_node

        # Ask the user if they want to save the tree to a file
        save_tree = input("Do you want to save your search results to a file? Yes or No? ")

        if save_tree.lower() == "yes":
            # Get the filename from the user
            filename = input("Enter the filename to save the tree to: ")

            # Save the entire tree to the file
            with open(filename, "w") as f:
                f.write(tree_to_string(root_node))

            print(f"Tree saved to {filename}")
            break
        else:
            print("Tree not saved.")










