import React from 'react';

const Sorter = ({ handleSortChange, sortOption }) => {
    return (
        <>
            <label htmlFor="sort">Sort by: </label>
            <select 
                id="sort" 
                value={sortOption} 
                onChange={(e) => handleSortChange(e.target.value)}
                className="px-3 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
                <option value="count">Count</option>
                <option value="alphabet">Alphabetical</option>
            </select>
        </>
    );
};

export default Sorter;