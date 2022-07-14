import { useSelector } from "react-redux";

function Wordlist() {

    const {data} = useSelector((state) => state.wordData)

    return (
        <div className="wordlist mx-auto w-8/12">
            {   data.wordlist ? 
                data.wordlist.map((item,key) => {
                    return(
                        <p key={key} className={`text-blue-500 word ${item.type} ${item.oxford}`}> {item.word} <b>{item.count}</b></p>
                    )}
               ) :
               null
            }
        </div>
    )
}

export default Wordlist