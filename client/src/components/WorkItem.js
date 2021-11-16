import React from "react";
import ProgressStateTextBox from "./ProgressStateTextBox";
import ButtonControl from "./ButtonControl";
import * as R from "../Resources";
import cfg from "../config"
import axios from "axios";
import {CollectTargetName} from "../Resources";

class WorkItem extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            item: props.value,
            opacity: 1.0,
            backgroundColor: '#FFFFFF',
        };
        this.handleMouseHover = this.handleMouseHover.bind(this);
        this.handleMouseLeave = this.handleMouseLeave.bind(this);
    }

    handleMouseHover() { this.setState(this.toggleHoverState); }
    handleMouseLeave() { this.setState(this.toggleLeaveState); }

    toggleHoverState(state) { return { opacity: 0.5, backgroundColor: '#EEEEEE' }; }
    toggleLeaveState(state) { return { opacity: 1.0, backgroundColor: '#FFFFFF' }; }

    componentDidUpdate(prevProps, prevState, snapshot) {
        // console.log(prevProps.value)
        this.state.item = prevProps.value
    }

    attach() {
        const request = async () => {
            // alert(this.state.item.id)
            let data = { id: this.state.item.id };
            const response = await axios.post(`http://${cfg.host}:${cfg.proxyPort}/action/attach_work`, data);
            if (response.status !== 200) {
                alert('요청한 작업을 수행할 수 없습니다.');
            } else {
                // alert('처리되었습니다.');
                this.setState( { value: R.STATE_ATTACHED } )
                window.location.reload();
            }
        };
        request()
    }

    stop() {

        const currentState = this.state.item.work_state;
        if(currentState !== R.STATE_ATTACHED && currentState !== R.STATE_WORKING) {
            alert('진행 상태가 아닐 때는 사용할 수 없습니다.');
            return;
        }

        const request = async () => {
            let data = { id: this.state.item.id };
            const response = await axios.post(`http://${cfg.host}:${cfg.proxyPort}/action/stop_work`, data);
            if (response.status !== 200) {
                alert('요청한 작업을 수행할 수 없습니다.');
            } else {
                // alert('처리되었습니다.');
                this.setState( { value: R.STATE_STOPPED } );
                window.location.reload();
            }
        };
        request()
    }

    terminate() {

        const currentState = this.state.item.work_state;
        if(currentState !== R.STATE_STOPPED) {
            alert('멈춤 상태가 아닐 때는 사용할 수 없습니다.');
            return;
        }

        const request = async () => {
            let data = { id: this.state.item.id };
            const response = await axios.post(`http://${cfg.host}:${cfg.proxyPort}/action/terminate_work`, data);
            if (response.status !== 200) {
                alert('요청한 작업을 수행할 수 없습니다.');
            } else {
                // alert('처리되었습니다.');
                this.setState( { value: R.STATE_DEATTACHED } );
                window.location.reload();
            }
        };
        request()
    }

    error() { this.setState( { value: R.STATE_ERROR } ) }

    renderProgressStateTextBox() {
        return <ProgressStateTextBox
            value={this.state.item.work_state}
        />;
    }

    renderButtonAttach() {
        return <ButtonControl
            value={ R.STATE_WAITING }
            workState = {this.state.item.work_state}
            groupdId = {this.state.item.id}
            onClick={()=> this.attach()}
        />
    }

    renderButtonStop() {
        return <ButtonControl
            value={ R.STATE_WORKING }
            workState = {this.state.item.work_state}
            groupdId = {this.state.item.id}
            onClick={()=> this.stop()}
        />
    }

    renderButtonTerminate() {
        return <ButtonControl
            value={ R.STATE_TERMINATED }
            workState = {this.state.item.work_state}
            groupdId = {this.state.item.id}
            onClick={()=> this.terminate()}
        />
    }


    render() {

        const secs = this.state.item.update_time;
        var hour   = "00"
        var minute = "00"
        var second = "00"
        let timeView, controlView, collectionState
        let itemViewHeight = 220
        if (this.state.item.work_state === R.STATE_WAITING) {
            controlView = this.renderButtonAttach()
        }

        if (this.state.item.work_state === R.STATE_ATTACHED) {

            const hourNum = Math.floor(secs / 3600);
            const hourMod = secs % 3600;
            const minuteNum = Math.floor(hourMod / 60);
            const minuteMod = hourMod % 60;

            hour   = (hourNum < 10 ? '0':'') + hourNum;
            minute = (minuteNum < 10 ? '0':'') + minuteNum;
            second = (minuteMod < 10 ? '0':'') + Math.floor(minuteMod);

            timeView = <div style={{ paddingTop:6, paddingLeft: 20, fontSize:16, color: '#7F7F7F' }}>
                경과시간:&nbsp;<label style={{color:'#ff9e01', fontSize:16}}>{hour}:{minute}:{second}</label>
            </div>

            controlView = this.renderButtonStop()
        }

        if (this.state.item.work_state === R.STATE_WORKING) {

            const hourNum = Math.floor(secs / 3600);
            const hourMod = secs % 3600;
            const minuteNum = Math.floor(hourMod / 60);
            const minuteMod = hourMod % 60;

            hour   = (hourNum < 10 ? '0':'') + hourNum;
            minute = (minuteNum < 10 ? '0':'') + minuteNum;
            second = (minuteMod < 10 ? '0':'') + Math.floor(minuteMod);

            timeView = <div style={{ paddingTop:8, paddingLeft: 20, fontSize:16, color: '#7F7F7F' }}>
                경과시간:&nbsp;<label style={{color:'#ff9e01', fontSize:16}}>{hour}:{minute}:{second}</label>
            </div>
            controlView = this.renderButtonStop()
        }

        if (this.state.item.work_state === R.STATE_STOPPED) {
            controlView = this.renderButtonTerminate()
        }

        if (this.state.item.work_state === R.STATE_WORKING || this.state.item.work_state === R.STATE_STOPPED) {
            let total_html_file_count = 0
            let total_csv_line_count = 0
            const report = this.state.item.report;
            for (const channel in report) {
                total_html_file_count += report[channel].html_file_count
                total_csv_line_count += report[channel].csv_line_count
            }
            collectionState =
                <div>&nbsp;&nbsp;HTML문서 <font color={"#00b050"}>{total_html_file_count}</font>건 수집,
                추출된 텍스트 <font color={"#FF4E00"}>{total_csv_line_count}</font>줄</div>

        } else {
            collectionState = <div>&nbsp;&nbsp;-</div>
        }

        let channelsTxt = ''
        const channelArr = this.state.item.channels.split(',')
        for (let index = 0; index < channelArr.length; index++) {
            const channel = channelArr[index]
            channelsTxt += R.CollectTargetName[channel]
            if (index < channelArr.length -1)
                channelsTxt += ', '
        }
        let channelListText = <div>{channelsTxt}</div>

        return (
        <div
            onMouseEnter={this.handleMouseHover}
            onMouseLeave={this.handleMouseLeave}
            onClick={(e) => {
                this.props.openPopup();
            }}
            style={{
                position: 'relative', width: '100%', height: itemViewHeight,
                backgroundColor: this.state.backgroundColor,
                borderBottom: '1px solid #AEAEAE', display: 'flex', cursor: 'pointer' }}>
            <div>
                <div style={{ position: 'absolute', top:'10%', left: '2%', display: 'flex' }}>
                    {this.renderProgressStateTextBox()}
                    {timeView}
                </div>
                <div style={{ position: 'absolute', top:'30%', left: '2%', display: 'flex', fontSize: '12pt' }}>
                    <font color={"#7F7F7F"}>수집현황: </font>
                    {collectionState}
                </div>
                <div
                    style={{ position: 'absolute', top:'43%', left: '2%', display: 'flex', fontSize: '12pt' }}>
                    <font color={"#7F7F7F"}>수집채널: </font>
                    &nbsp;&nbsp;{channelListText}
                </div>
                <div style={{ position: 'absolute', top:'56%', left: '2%', display: 'flex', fontSize: '12pt' }}>
                    <font color={"#7F7F7F"}>키워드: </font>
                    &nbsp;&nbsp;{this.state.item.keywords}
                </div>
                <div style={{ position: 'absolute', top:'69%', left: '2%', display: 'flex', fontSize: '12pt' }}>
                    <font color={"#7F7F7F"}>수집기간: </font>
                    &nbsp;&nbsp;{this.state.item.start_date.split(' ')[0]}
                    &nbsp;~&nbsp;{this.state.item.end_date.split(' ')[0]}
                </div>
                <div style={{ position: 'absolute', top:'82%', left: '2%', display: 'flex', fontSize: '12pt' }}>
                    <font color={"#7F7F7F"}>설명: </font>
                    &nbsp;&nbsp;{this.state.item.title}
                </div>
            </div>

            <div style={{
                position: 'absolute', top: '50%', left: '86%',
                transform: 'translate(-20%, -50%)', display: 'flex' }}>
                {controlView}
            </div>
        </div>
        );
    }
}

export default WorkItem;