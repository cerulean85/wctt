import React from 'react';

class Header extends React.Component {
    render() {
        return (
            <div
                style={{
                    margin: 'auto',
                    width: '80%',
                    height: 80,
                    borderTop: '1px solid black',
                    paddingTop: 50,
                    fontSize: 40
                }}
            >BIG DATA COLLECTION
            </div>
        )
    }
}

export default Header;