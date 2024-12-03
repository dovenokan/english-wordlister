import React from 'react';

const Pagination = ({ currentPage, totalPages, handlePreviousPage, handleNextPage }) => {
    return (
        <>
            <button 
                onClick={handlePreviousPage} 
                disabled={currentPage === 1}
                className="px-4 py-2 bg-blue-500 text-white rounded-md transition-colors duration-200 
                           hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
                Previous
            </button>
            <span className="text-gray-700 font-medium">
                Page {currentPage} of {totalPages}
            </span>
            <button 
                onClick={handleNextPage} 
                disabled={currentPage === totalPages}
                className="px-4 py-2 bg-blue-500 text-white rounded-md transition-colors duration-200 
                           hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
                Next
            </button>
        </>
    );
};

export default Pagination;