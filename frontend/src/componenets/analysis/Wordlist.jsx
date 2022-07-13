import { useSelector } from "react-redux";

function Wordlist() {

    const {data} = useSelector((state) => state.wordData)

    return (
        <div className="wordlist">
            {
                data.wordlist.map((item) => {
                    return(
                        <p className="text-blue-500">{item.word}</p>
                    )}
                        
                ) 
            }
        </div>
    )
}

export default Wordlist