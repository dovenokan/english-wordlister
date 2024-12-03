import Wordlist from './Wordlist'
import Loading from '../misc/Loading'
import { useSelector } from "react-redux";
import { useState } from "react";
import Sorter from '../common/Sorter';

function Analysis() {

  const { wordlist_loading } = useSelector((state) => state.wordData);
  const [sortOption, setSortOption] = useState('count');

  const handleSortChange = (newSortOption) => {
      setSortOption(newSortOption);
  };

  if (wordlist_loading) {
    return (
    	<Loading />
    )
  } else {
    return (
      <div className="analysis mb-8">
        <Wordlist sortOption={sortOption} />
      </div>
    )
  }
}

export default Analysis