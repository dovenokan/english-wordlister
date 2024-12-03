import { useSelector } from "react-redux";
import { useState } from 'react';
import Sorter from '../common/Sorter';
import Pagination from '../common/Pagination';

function Wordlist() {

    const { data } = useSelector((state) => state.wordData);
    const [currentPage, setCurrentPage] = useState(1);
    const [sortOption, setSortOption] = useState('count');
    const wordsPerPage = 10;

    const sortedWords = data.wordlist ? [...data.wordlist].sort((a, b) => {
        if (sortOption === 'count') {
            return b.count - a.count;
        } else if (sortOption === 'alphabet') {
            return a.word.localeCompare(b.word);
        }
        return 0;
    }) : [];

    const indexOfLastWord = currentPage * wordsPerPage;
    const indexOfFirstWord = indexOfLastWord - wordsPerPage;
    const currentWords = sortedWords.slice(indexOfFirstWord, indexOfLastWord);

    const totalPages = Math.ceil(sortedWords.length / wordsPerPage);

    const handleNextPage = () => {
        if (currentPage < totalPages) {
            setCurrentPage(currentPage + 1);
        }
    };

    const handlePreviousPage = () => {
        if (currentPage > 1) {
            setCurrentPage(currentPage - 1);
        }
    };

    const handleSortChange = (newSortOption) => {
        setSortOption(newSortOption);
        setCurrentPage(1); // Reset to first page on sort change
    };

    return (
        <div className="wordlist-body">
            <div className="sort-controls flex items-center justify-center space-x-4 mb-4 p-2 bg-gray-100 rounded-lg">
                <Sorter 
                    handleSortChange={handleSortChange} 
                    sortOption={sortOption} 
                />
            </div>

            <div className="wordlist-container relative">
                <div className="wordlist mx-auto w-8/12">
                    {currentWords.map((item, key) => (
                        <p key={key} className={`text-blue-500 word ${item.type} ${item.oxford}`}> {item.word} <b>{item.count}</b></p>
                    ))}
                </div>

                <div className="pagination-controls absolute bottom-0 left-1/2 transform -translate-x-1/2 w-full flex justify-center mt-4 p-2 bg-gray-100 rounded-lg">
                    <Pagination 
                        currentPage={currentPage}
                        totalPages={totalPages}
                        handlePreviousPage={handlePreviousPage}
                        handleNextPage={handleNextPage}
                    />
                </div>
            </div>
        </div>
    );
}

export default Wordlist;