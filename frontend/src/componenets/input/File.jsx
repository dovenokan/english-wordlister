import React from 'react'

function File({show}) {
  if (show) {
      return (
        <div className="file">
            <input type="file" name="" id="" />
        </div>
      )
  } else {
      return (
        null
      )
  }
}

export default File