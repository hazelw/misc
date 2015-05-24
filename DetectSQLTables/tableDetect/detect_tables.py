import sys, re, copy
__author__ = 'Hazel'

class TableFinder:

    '''
    Takes an argument of a relative path + sql file name from the command line, then returns the tables mentioned in
    that file.
    '''

    def __init__(self, file_path):
        '''
        :param file_path: (relative) file path posted by the user on the command line
        :return: nil

        Prints the names of the tables referenced in the SQL file loaded from file_path
        '''
        table_names = set()

        with open(file_path, mode='r', encoding='utf-8') as sql_file:
            file_contents = sql_file.read()
            file_contents = file_contents.replace('\n', ' ').upper()
            words = file_contents.split(' ')

            # finding all table and alias names
            for word in words:
                if word.isalnum():
                    possible_patterns = self.get_possible_table_patterns(word)
                    for possible_pattern in possible_patterns:
                        pattern = re.compile(possible_pattern)
                        if len(pattern.findall(file_contents)) > 0:
                            table_names.add(word)

            # removing all alias names
            table_names_copy = copy.copy(table_names)

            for word in table_names_copy:
                for table in table_names_copy:
                    possible_alias_patterns = self.get_possible_alias_patterns(word,table)
                    for possible_alias_pattern in possible_alias_patterns:
                        pattern = re.compile(possible_alias_pattern)
                        if len(pattern.findall(file_contents)) > 0 and word in table_names:
                            table_names.remove(word)

            print(table_names)


    def get_possible_table_patterns(self, current_word):
        '''
        :param current_word: the current word being inspected
        :return: set of regular expression rules, one of which will be true if the word is a table name or alias for
        a table
        '''
        possible_patterns = []
        possible_patterns.append('FROM ' + current_word)
        possible_patterns.append('TABLE ' + current_word)
        possible_patterns.append('INDEX .* ON ' + current_word)
        # TODO: decide whether to include views
        # possible_patterns.append('VIEW ' + current_word)
        possible_patterns.append('INSERT INTO ' + current_word)
        possible_patterns.append('JOIN ' + current_word)
        possible_patterns.append('UPDATE ' + current_word + ' SET')

        return possible_patterns

    def get_possible_alias_patterns(self, current_word, current_table):
        '''
        :param current_word: current word being inspected
        :param current_table: a table/alias previously detected
        :return: set of regular expression rules, one of which will be true if the current word is an alias for the
        current table
        '''
        possible_patterns = []
        possible_patterns.append(current_table + '.' + current_word)
        possible_patterns.append(current_table + ' ' + current_word)
        return possible_patterns

TableFinder(sys.argv[1])

