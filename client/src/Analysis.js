//cafe
import React, { Component } from "react";
import PopupWorkCreate from "./components/PopupWorkCreate";
import axios from "axios";
import cfg from "./config";
import ProgressStateTextBox from "./components/ProgressStateTextBox";
import * as R from "./Resources";
import moment from "moment";
import CheckboxTarget from "./components/CheckboxTarget";

class Analysis extends React.Component{
    constructor(props) {
        super();
        this.state = {
            item: {},
            morphNoun: false,
            morphAdj: false,
            tableTF: false,
            tableTFIDF: false,
            tableTCOO: false
        }
    }

    update() {
        const data = {
            id: this.props.workGroupId
        }
        axios.post(`http://${cfg.host}:${cfg.proxyPort}/action/get_work_group`, data).then( (response) => {
            if (response.data.totalCount > 0) {
                const item = response.data.list[0]
                this.setState({item: item})
            }
        });
    }

    componentDidMount() {
        this.update();
        // this.updateID = setInterval(
        //     () => this.update(),
        //     3000
        // );
    }

    onNameChanged = (d) => {
        this.state.item.name = d.target.value;
        this.setState({
            item: this.state.item,
        })
    };

    renderProgressStateTextBox() {
        return <ProgressStateTextBox
            value={this.state.item.work_state}
        />;
    }

    openSaveDir() {

        const data = {
            data_directory: this.state.item.data_directory + "\\csv\\" + this.state.item.id
        }

        axios.post('http://localhost:3001/action/open_directory', data).then( (response) => {
        });
    }

    executeFile(filename) {
        const data = {
            data_directory: this.state.item.data_directory + "\\csv\\" + this.state.item.id + "\\df.csv",
        }
        // alert(this.state.item.data_directory + "\\csv\\" + this.state.item.id + "\\" + filename)
        axios.post('http://localhost:3001/action/execute_file', data).then( (response) => {
        });
    }

    extractMorphs = () => {
        const data = {
            id: this.state.item.id,
            kindsOf: String(this.state.morphNoun === true ? 1: 0) + String(this.state.morphAdj === true ? 1: 0),
            data_directory: this.state.item.data_directory + "\\csv\\" + this.state.item.id + "\\df.csv"
        }
        axios.post('http://localhost:3001/action/extract_morphs', data).then( (response) => {
        });
    }

    removeStopwords = () => {
        const data = {
            id: this.state.item.id,
            kindsOf: String(this.state.morphNoun === true ? 1: 0) + String(this.state.morphAdj === true ? 1: 0),
            data_directory: this.state.item.proj_directory + "\\client\\stopwords.txt"
        }
        axios.post('http://localhost:3001/action/remove_stopwords', data).then( (response) => {
        });
    }

    createTables() {
        const data = {
            id: this.state.item.id,
            kindsOf: String(this.state.tableTF === true ? 1: 0) +
                String(this.state.tableTFIDF === true ? 1: 0) +
                String(this.state.tableTCOO === true ? 1: 0),
            data_directory: this.state.item.data_directory + "\\csv\\" + this.state.item.id + "\\df.csv"
        }
        axios.post('http://localhost:3001/action/create_tables', data).then( (response) => {
        });
    }

    onTargetChanged = (d) => {
        const name = d.target.name;
        const value = this.state[name];
        this.setState({ [name]: !value })
    };

    render(){
        let targets = '';
        const channels = this.state.item.channels
        if (channels === undefined) return <div></div>

        const channelArr = this.state.item.channels.split(',');
        for(let i=0; i<channelArr.length; i++) {
            const channel = channelArr[i];
            if(channel === undefined || channel === '') continue;
            targets += R.CollectTargetName[channel] + "\u00A0\u00A0\u00A0\u00A0";
        }

        let total_html_file_count = 0
        let total_csv_line_count = 0
        const report = this.state.item.report;
        console.log(report)
        let reportArr = []
        for (const channel in report) {
            total_html_file_count += report[channel].html_file_count
            total_csv_line_count += report[channel].csv_line_count
            reportArr.push({
                channelName: R.CollectTargetName[channel],
                htmlFileCount: report[channel].html_file_count,
                csvLineCount: report[channel].csv_line_count
            })
        }

        const collectionState =
            <div style={{marginTop:6}}>- HTML??????&nbsp;<font color={"#00b050"}>{total_html_file_count}</font>??? ??????,
                ????????? ????????? <font color={"#FF4E00"}>{total_csv_line_count}</font>???</div>

        const dataDir = this.state.item.data_directory
        // eslint-disable-next-line no-unused-expressions
        let collectionDetail = <div></div>
        const currentState = this.state.item.work_state;
        if(reportArr.length > 0 && (currentState === R.STATE_ATTACHED || currentState === R.STATE_WORKING)) {

            collectionDetail =
                <div style={{
                    fontSize: 18,
                }}>
                    <div style={{textAlign:'left'}}>
                        <div>
                            <table>
                                <thead style={{border: "1px solid #54585d"}}>
                                <tr>
                                    <td width={100}>?????? ??????</td>
                                    <td width={100}>HTML ??????(???)</td>
                                    <td width={100}>????????? ?????????(???)</td>
                                </tr>
                                </thead>
                                <tbody>
                                {
                                    reportArr.map(report =>
                                        <tr>
                                            <td width={100}><font color={"#54585d"}>{report.channelName}</font></td>
                                            <td width={100} style={{textAlign:'center'}}><font color={"#00b050"}>{report.htmlFileCount}</font></td>
                                            <td width={100} style={{textAlign:'center'}}><font color={"#FF4E00"}>{report.csvLineCount}</font></td>
                                        </tr>
                                    )
                                }
                                <tr>
                                    <td width={100}><font color={"#000000"}>??????</font></td>
                                    <td width={100} style={{textAlign:'center'}}><font color={"#0000FF"}>{total_html_file_count}</font></td>
                                    <td width={100} style={{textAlign:'center'}}><font color={"#0000FF"}>{total_csv_line_count}</font></td>
                                </tr>
                                </tbody>
                            </table>
                        </div>
                        {/*<div>*/}
                        {/*    {*/}
                        {/*        reportArr.map(report =>*/}
                        {/*            <table>*/}
                        {/*                <tr>*/}
                        {/*                    <td width={'25%'}><font color={"#aaaaaa"}>{report.channelName}</font></td>*/}
                        {/*                    <td width={'25%'} style={{textAlign:'center'}}><font color={"#00b050"}>{report.htmlFileCount}</font></td>*/}
                        {/*                    <td width={'25%'} style={{textAlign:'center'}}><font color={"#FF4E00"}>{report.csvLineCount}</font></td>*/}
                        {/*                </tr>*/}
                        {/*            </table>*/}
                        {/*        )*/}
                        {/*    }*/}
                        {/*</div>*/}
                    </div>
                </div>
        }

        const data_directory = this.state.item.data_directory.replaceAll("\\", "/")  + '/csv/' + this.state.item.id

        return(
            <div style={{
                marginTop: 20,
                marginLeft: 30,
                marginRight: 30,
                marginBottom: 40,
                color: "#1F1F1F",
                textAlign: "left",
                borderBottom: '1px solid #000000'
            }}>

                <div className="contents-text-outer">
                    <div className="contents-text-inner">
                        <label style={{fontSize: 21, fontWeight:'bold'}}>?????? ?????????</label>
                        &nbsp;&nbsp;<button onClick={this.props.prev} style={{height: 30}}>????????????</button>
                    </div>
                </div>

                <hr width={"100%"} color={"#555555"}/>

                <div className="sub-title-box">
                    <div className="sub-title-outer" style={{width:'12%'}}>
                        <div className="sub-title-inner">?????????</div>
                    </div>

                    <div className="contents-text-outer">
                        <div className="contents-text-inner">
                            {this.state.item.title}
                        </div>
                    </div>
                </div>

                <div className="sub-title-box" style={{borderBottom: "1px solid #808080", marginBottom: 10}}/>

                <div className="sub-title-box">
                    <div className="sub-title-outer" style={{width:'12%'}}>
                        <div className="sub-title-inner">?????????</div>
                    </div>
                    <div className="contents-text-outer">
                        <div className="contents-text-inner">
                            {this.state.item.keywords}
                        </div>
                    </div>
                </div>

                <div className="sub-title-box" style={{borderBottom: "1px solid #808080", marginBottom: 10}}/>

                <div className="sub-title-box">
                    <div className="sub-title-outer" style={{width:'12%'}}>
                        <div className="sub-title-inner">?????? ??????</div>
                    </div>

                    <div className="contents-text-outer">
                        <div className="contents-text-inner">
                            {moment(this.state.item.start_date).format('YYYY-MM-DD')}&nbsp;~&nbsp;{moment(this.state.item.end_date).format('YYYY-MM-DD')}
                        </div>
                    </div>
                </div>

                <div className="sub-title-box" style={{borderBottom: "1px solid #808080", marginBottom: 10}}/>

                <div className="sub-title-box">
                    <div className="sub-title-outer" style={{width:'12%'}}>
                        <div className="sub-title-inner">?????? ??????</div>
                    </div>
                    <div className="contents-text-outer">
                        <div className="contents-text-inner">
                            {targets}
                        </div>
                    </div>
                </div>

                <div className="sub-title-box" style={{borderBottom: "1px solid #808080", marginBottom: 10}}/>

                <div className="sub-title-box">
                    <div className="sub-title-outer" style={{width:'12%'}}>
                        <div className="sub-title-inner">?????????</div>
                    </div>
                    <div style={{width:10 }}/>
                    <div style={{fontSize: 14, textAlign:'left', display:'flex'}}>
                        <ul style={{lineHeight: 1.8, paddingLeft: 20}}>
                            <li>
                                <div>
                                    <button style={{
                                        fontSize:14, cursor:'pointer', height: 50, borderRadius: 5,
                                        backgroundColor:'#0099FF', color: '#FFFFFF', border:'0px'}}
                                            onClick={this.extractMorphs}>????????? ??????
                                    </button>
                                    <div style={{fontSize:12, marginTop: 5}}>- ????????? ???????????? ????????? ??? ??????????????????.</div>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>

                <div className="sub-title-box" style={{borderBottom: "1px solid #808080", marginBottom: 10}}/>

                <div className="sub-title-box">
                    <div className="sub-title-outer" style={{width:'12%'}}>
                        <div className="sub-title-inner">?????? ??????</div>
                    </div>
                    <div style={{width:10 }}/>

                    <div style={{fontSize: 14, textAlign:'left', display:'flex'}}>
                        <ul style={{lineHeight: 1.8, paddingLeft: 20}}>
                            <li>
                                <div>
                                    <button style={{
                                        fontSize:14, cursor:'pointer', height: 50, borderRadius: 5,
                                        backgroundColor:'#0099FF', color: '#FFFFFF', border:'0px'}}
                                            onClick={this.extractMorphs}>?????? ????????????
                                    </button>
                                    <div style={{fontSize:12, marginTop: 5}}>- ???????????? ???????????? ????????? ???????????????.</div>
                                </div>
                            </li>
                            <li style={{marginTop: 20}}>
                                <div style={{fontSize:16}}>?????? ?????? ??????</div>
                                <div style={{fontSize:12}}>
                                    - ????????????:<label style={{color:'#0099FF'}}>{data_directory}</label>
                                    &nbsp;&nbsp;<button className="open-btn" onClick={() => this.executeFile("tf_table.csv")}>??????</button>
                                </div>
                                <div style={{fontSize:12}}>- ?????????: <label style={{color:'#0099FF'}}>{"/ext_id_DATE.csv"}</label></div>
                            </li>

                        </ul>
                    </div>
                </div>
                <div className="sub-title-box" style={{borderBottom: "1px solid #000000", marginBottom: 10}}/>
                <div className="sub-title-box" style={{marginBottom: 10}}>
                    <div className="sub-title-outer" style={{width:'12%'}}>
                        <div className="sub-title-inner">????????? ??????</div>
                    </div>
                    <div style={{width:10 }}/>
                    <div style={{fontSize: 14, textAlign:'left', display:'flex'}}>
                        <ul style={{lineHeight: 1.8, paddingLeft: 20}}>
                            <li>
                                <div style={{fontSize:16}}>????????? ??????</div>
                                <div style={{fontSize:12}}>- ????????? ???????????? ????????? ??? ????????? ???????????? ????????? ???????????????.</div>
                                <div style={{marginTop: 5, marginBottom: 20}}>
                                    <div style={{ textAlign: 'left', height:30, display:'flex'}}>
                                        <CheckboxTarget
                                            name={"tableTF"}
                                            style={{width:150, height:20}}
                                            text={"??????-?????? ????????? (Term-Frequency Table; TF Table)"}
                                            checked={this.state.tableTF}
                                            onChanged={this.onTargetChanged}
                                        />
                                    </div>
                                    <div style={{ textAlign: 'left', height:30, display:'flex'}}>
                                        <CheckboxTarget
                                            name={"tableTF"}
                                            style={{width:150, height:20}}
                                            text={"TF-IDF ????????? (Term Frequency-Inverse Document Frequency Table)"}
                                            checked={this.state.tableTFIDF}
                                            onChanged={this.onTargetChanged}
                                        />
                                    </div>
                                    <div style={{ textAlign: 'left', height:30, display:'flex'}}>
                                        <CheckboxTarget
                                            name={"tableTCOO"}
                                            style={{width:150, height:20}}
                                            text={"?????? ?????? ?????? ?????? (Term Co-Occurrence Matrix)"}
                                            checked={this.state.tableTCOO}
                                            onChanged={this.onTargetChanged}
                                        />
                                    </div>
                                </div>
                                <button style={{
                                    fontSize:14, cursor:'pointer', height: 50, borderRadius: 5,
                                    backgroundColor:'#0099FF', color: '#FFFFFF', border:'0px'}}
                                        onClick={this.createTables}>????????? ????????????
                                </button>
                            </li>
                            <li style={{marginTop: 20}}>
                                <div style={{fontSize:16}}>????????? ?????? ??????</div>

                                <div style={{fontSize:12}}>
                                    - ??????-?????? ?????????: <label style={{color:'#0099FF'}}>{data_directory + "/xx_tf_table.csv"}</label>
                                    &nbsp;&nbsp;<button className="open-btn" onClick={() => this.executeFile("tf_table.csv")}>??????</button>
                                </div>
                                <div style={{fontSize:12}}>
                                    - TF-IDF ?????????: <label style={{color:'#0099FF'}}>{data_directory + "/xx_tf_idf_table.csv"}</label>
                                    &nbsp;&nbsp;<button className="open-btn" onClick={() => this.executeFile("tf_idf_table.csv")}>??????</button>
                                </div>
                                <div style={{fontSize:12}}>
                                    - ?????? ?????? ?????? ??????: <label style={{color:'#0099FF'}}>{data_directory + "/xx_tf_coo_matrix.csv"}</label>
                                    &nbsp;&nbsp;<button className="open-btn" onClick={() => this.executeFile("tf_coo_matrix.csv")}>??????</button>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        )
    }
}

export default Analysis;