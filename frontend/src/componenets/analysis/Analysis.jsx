import Wordlist from './Wordlist'
import Loading from '../misc/Loading'
import { useSelector } from "react-redux";

function Analysis() {

  const { wordlist_loading } = useSelector((state) => state.wordData);

  if (wordlist_loading) {
    return (
    	<Loading />
    )
  } else {
    return (
      <div className="analysis">
        <Wordlist />
      </div>
    )
  }
}

export default Analysis