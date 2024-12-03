import { useSelector } from "react-redux";

function Stats() {
  const { data, cargo } = useSelector((state) => state.wordData);

  const getWordCount = () => {
    return data.wordlist ? data.wordlist.length : 0;
  };

  const getTypeStats = () => {
    if (!data.wordlist) return { count: 0, types: {} };
    
    const stats = data.wordlist.reduce((acc, word) => {
      acc.types[word.type] = (acc.types[word.type] || 0) + 1;
      acc.count += 1;
      return acc;
    }, { count: 0, types: {} });

    return stats;
  };

  const getAverageWordLength = () => {
    if (!data.wordlist || !data.wordlist.length) return 0;
    const totalLength = data.wordlist.reduce((sum, word) => sum + word.word.length, 0);
    return (totalLength / data.wordlist.length).toFixed(1);
  };

  const stats = getTypeStats();
  const avgLength = getAverageWordLength();

  if (!cargo.trim()) {
    return null;
  }

  return (
    <div className="statistics-box">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 rounded-lg">
        <div className="stats-breakdown col-span-full">
          <table className="w-full bg-white rounded-lg shadow-md overflow-hidden">
            <thead className="bg-gray-200">
              <tr>
                <th className="p-3 text-left">Word Type</th>
                <th className="p-3 text-right">Count</th>
                <th className="p-3 text-right">Percentage</th>
                <th className="p-3 text-left">Visualization</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(stats.types).map(([type, count]) => {
                const percentage = ((count / stats.count) * 100).toFixed(1);
                const color = getTypeColor(type);
                return (
                  <tr key={type} className="border-b">
                    <td className="p-3 font-medium" style={{color}}>{type}</td>
                    <td className="p-3 text-right">{count}</td>
                    <td className="p-3 text-right">{percentage}%</td>
                    <td className="p-3">
                      <div 
                        className="h-2 rounded" 
                        style={{
                          width: `${percentage}%`, 
                          backgroundColor: color
                        }}
                      />
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

function getTypeColor(type) {
  const colors = {
    verb: '#4285f4',
    adj: '#0f9d58',
    noun: '#db4437',
    phrverb: '#f4b400',
    undef: '#666'
  };
  return colors[type] || '#666';
}

export default Stats;
