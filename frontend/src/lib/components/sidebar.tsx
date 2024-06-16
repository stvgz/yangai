import React from 'react';

const Sidebar = ({ textSize, content }) => {
    const style = {
        backgroundColor: 'white',
        color: 'black',
        fontSize: textSize
    };

    return (
        <div style={style}>
            {content.map((item, index) => (
                <div key={index}>{item}</div>
            ))}
        </div>
    );
};

export default Sidebar;