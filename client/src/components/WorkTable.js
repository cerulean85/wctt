import React from "react";
import WorkItem from "./WorkItem";
import cfg from "../config"
import axios from "axios";
import PopupWorkDetail from "./PopupWorkDetail";

class WorkTable extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            list: [],
            isOpen: false,
            date: new Date(),
            message: "작업 목록을 불러오는 중입니다.",
            popupItem: {}
        };
    }

    componentDidMount() {
        this.updateID = setInterval(
            () => this.update(),
            3000
        );
    }

    update() {
        this.getWorGroupList();
    }

    componentWillUnmount() {
        clearInterval(this.updateID);
    }

    openPopup = (item) => {
        this.setState({isOpen: !this.state.isOpen, popupItem: item})
    };

    closePopup = () => {
        this.setState({isOpen: false})
    };

    getWorGroupList = () => {
        axios.post(`http://${cfg.host}:${cfg.proxyPort}/action/get_work_group_list`).then( (response) => {
            const list = response.data.list;
            this.setState({list: list})
            if (list.length === 0)
                this.setState({message: "수집 작업이 존재하지 않습니다."})
        });
    };

    render() {

        let listItems = <div
            style={{
                // margin: 'auto',
                height: 120,
                marginTop: 80,
                fontSize: 18,
                borderBottom: '1px solid #AEAEAE',
                color: '#AEAEAE',
            }}>
            {this.state.message}</div>
        if(this.state.list.length > 0) {
            listItems = this.state.list.map((item) =>
                // <WorkItem value={item} openPopup={this.openPopup.bind(this, item)}/>
                <WorkItem value={item} detail={this.props.detail}/>
            );
        }

        return (

            <div>

                {listItems}

                {/*{this.state.isOpen && <PopupWorkDetail*/}
                {/*    item={this.state.popupItem}*/}
                {/*    content={<>*/}
                {/*    </>}*/}
                {/*    handleClose={this.closePopup}*/}
                {/*/>}*/}
            </div>
        );
    }
}

export default WorkTable;