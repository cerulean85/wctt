import React, { Component, useState } from "react";
import * as R from "./Resources";
import {Button} from "semantic-ui-react";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
} from "react-router-dom";
import Page01 from "./documents/page01";
import Page02 from "./documents/page02";
import Page03 from "./documents/page03";

const menuList = {
    0: <Page01 />,
    1: <Page02 />,
    2: <Page03 />
}

class Docs extends React.Component{
    constructor(props) {
        super();

        this.state = {
            menu: 0,
        };
    }

    changeMenu = (menuIndex) =>{
        this.setState({menu : menuIndex})
    }

    render(){
        return(
            <div>
                <div style={{float:"left", width:"20%", backgroundColor:"#dee2e6", height:"100%", minHeight:400}}>
                    <h2 align="center">목&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;차</h2>
                    <ul style={{lineHeight: 1.8}}>
                        <li style={{cursor:"pointer"}} className={`${this.state.menu === 0? 'active': ''}`} onClick={() => this.changeMenu(0)}>01. WCTT 설치</li>
                        <li style={{cursor:"pointer"}} className={`${this.state.menu === 1? 'active': ''}`} onClick={() => this.changeMenu(1)}>02. 수집 작업 등록 및 조작</li>
                        <li style={{cursor:"pointer"}} className={`${this.state.menu === 2? 'active': ''}`} onClick={() => this.changeMenu(2)}>03. 수집 데이터 확인</li>
                    </ul>
                </div>
                <div style={{float:"right", width:"80%"}} className="contentArea">{menuList[this.state.menu]}</div>
            </div>
        )
    }
}

export default Docs;