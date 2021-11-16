import './App.css';
import React, { useState } from "react";
import ButtonOpenAddWorkWindow from "./components/ButtonOpenAddWorkWindow";
import * as R from "./Resources";
import Header from './components/Header'
import WorkTable from "./components/WorkTable";
import PopupWorkCreate from "./components/PopupWorkCreate"
import Collection from './Collection';
import Analysis from './Analysis';
import About from './About';
import Docs from './Docs';

const menuList = {
    0: <Collection />,
    1: <About />,
    2: <Docs />
}

class App extends React.Component {
    constructor(props) {
        super(props);
        this.handleMouseHover = this.handleMouseHover.bind(this);
        this.handleMouseLeave = this.handleMouseLeave.bind(this);
        this.state = {
            isOpen: false,
            menu: 0,
            backgroundColor: '#0046C0',
            date: new Date(),
            opacity: 1.0,
        }
        this.togglePopup = this.togglePopup.bind(this)
    }

    handleMouseHover() { this.setState(this.toggleHoverState); }
    handleMouseLeave() { this.setState(this.toggleLeaveState); }

    toggleHoverState(state) { return { backgroundColor: '#323232' }; }
    toggleLeaveState(state) { return { backgroundColor: '#0046C0' }; }

    changeMenu = (menuIndex) =>{
        this.setState({menu : menuIndex})
    }

    jupyter = () => {
        window.open('http://localhost:8888/tree', '_blank')
    }

    togglePopup = () => {
        this.setState({isOpen: !this.state.isOpen})
    }

    tick() {
        this.setState({
            date: new Date()
        });
    }

    componentDidMount() {
        this.timerID = setInterval(
            () => this.tick(),
            1000
        );
    }

    render() {
        const jptimg = process.env.PUBLIC_URL + "/jupyter.png"
        return(

            <div>
                <div className="menuBar">
                    <div className="timeZone">
                        <div
                            style={{
                                fontWeight: 'bolder',
                                fontSize: 14,
                                width: 120,
                                height: 40,
                                paddingTop: 20,
                                marginRight: 20,
                                display: 'inline-block'
                            }}>
                            {/*{this.state.date.toLocaleTimeString()}*/}


                        </div>
                        {/*<div*/}
                        {/*    style={{*/}
                        {/*        float: "right",*/}
                        {/*        marginTop: 3,*/}
                        {/*        marginRight: 25,*/}
                        {/*    }}>*/}
                        {/*        <a href={"http://localhost:8888/tree"} target={"_blank"}>*/}
                        {/*            <img src={jptimg} width={50} height={50}/>*/}
                        {/*        </a>*/}
                        {/*</div>*/}
                        {/*<div*/}
                        {/*    onMouseEnter={this.handleMouseHover}*/}
                        {/*    onMouseLeave={this.handleMouseLeave}*/}
                        {/*    onClick={this.togglePopup}*/}
                        {/*    style={{*/}
                        {/*        fontWeight:'bolder',*/}
                        {/*        fontSize: 16,*/}
                        {/*        width: 120,*/}
                        {/*        height: 39,*/}
                        {/*        paddingTop: 20,*/}
                        {/*        marginRight: 20,*/}
                        {/*        textAlign: 'center',*/}
                        {/*        backgroundColor: this.state.backgroundColor,*/}
                        {/*        cursor: "pointer",*/}
                        {/*        display: 'inline-block',*/}
                        {/*        userSelect: "none",*/}
                        {/*        color: '#FFFFFF' }}>+&nbsp;ADD*/}
                        {/*</div>*/}
                    </div>

                    <ul className="tabs">
                        <li style={{
                            background: '#FFFFFF',
                            width: '50',
                            height: '150',
                            color: '#000000',
                            opacity: 1.0,
                            cursor: 'default'
                        }}>WCTT</li>

                        <li className={`${this.state.menu === 0? 'active': ''}`} onClick={() => this.changeMenu(0)}>Collection</li>
                        <li className={`${this.state.menu === 1? 'active': ''}`} onClick={() => this.changeMenu(1)}>About</li>
                        <li className={`${this.state.menu === 2? 'active': ''}`} onClick={() => this.changeMenu(2)}>Docs</li>
                    </ul>
                </div>

                <div className="contentArea">{menuList[this.state.menu]}</div>
                {this.state.isOpen && <PopupWorkCreate handleClose={this.togglePopup}/>}
            </div>


        )
    }
}
export default App;