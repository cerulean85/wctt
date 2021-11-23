import React, { Component } from "react";
import Collection from "./Collection";
import Analysis from "./Analysis";
import DetailWork from "./DetailWork";

class ProxyCollection extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            menu: 0,
            id: 0,
        };
    }

    changeMenu = (menuIndex) =>{
        this.setState({menu : menuIndex})
    }

    getMenu = (no) =>{
        if(no===0)
            return <Collection detail={this.goDetail}/>

        else if(no===1)
            return <DetailWork prev={this.goCollection} morph={this.goAnalysis} workGroupId={this.state.id}/>

        else if(no===2)
            return <Analysis prev={this.goCollection} workGroupId={this.state.id}/>
    }

    goCollection = () => {
        this.getMenu(0)
        this.setState({menu : 0})
    }

    goDetail = (id) => {

        this.getMenu(1)
        this.setState({menu : 1, id: id})
    }

    goAnalysis = (id) => {

        this.getMenu(2)
        this.setState({menu : 2, id: id})
    }

    render(){
        return (
            <div>
                <div className="contentArea">{this.getMenu(this.state.menu)}</div>
            </div>
        );
    }
}

export default ProxyCollection;