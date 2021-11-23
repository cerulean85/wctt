//cafe
import React, { Component } from "react";
import PopupWorkCreate from "./components/PopupWorkCreate";
import axios from "axios";
import cfg from "./config";
import ProgressStateTextBox from "./components/ProgressStateTextBox";
import * as R from "./Resources";
import moment from "moment";
import CheckboxTarget from "./components/CheckboxTarget";

class DetailWork extends React.Component{
    constructor(props) {
        super();
        this.state = {
            item: {},
            morphNoun: false,
            morphAdj: false,
            tableTF: false,
            tableTFIDF: false,
            tableTCOO: false,
            pageType: 0
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
        this.updateID = setInterval(
            () => this.update(),
            3000
        );
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
            data_directory: this.state.item.data_directory + "\\csv"
        }

        axios.post('http://localhost:3001/action/open_directory', data).then( (response) => {
        });
    }

    openSaveWeightsDir() {

        const data = {
            data_directory: this.state.item.data_directory + "\\csv\\weights"
        }

        axios.post('http://localhost:3001/action/open_directory', data).then( (response) => {
        });
    }

    executeFile(filename) {

        const data = {
            data_directory: this.state.item.data_directory + "\\csv\\" + filename,
        }

        // alert(this.state.item.data_directory + "\\csv\\" + this.state.item.id + "\\" + filename)
        axios.post('http://localhost:3001/action/execute_file', data).then( (response) => {
        });
    }

    extractMorphs = () => {
        const data = {
            id: this.state.item.id,
            data_directory: this.state.item.data_directory
        }
        axios.post('http://localhost:3001/action/extract_morphs', data).then( (response) => {
        });
    }

    createTables = () => {
        const data = {
            id: this.state.item.id,
            data_directory: this.state.item.data_directory,
            kindsOf: String(this.state.tableTF === true ? 1: 0) +
                String(this.state.tableTFIDF === true ? 1: 0) +
                String(this.state.tableTCOO === true ? 1: 0),
        }
        axios.post('http://localhost:3001/action/create_tables', data).then( (response) => {
        });
    }

    onTargetChanged = (d) => {
        const name = d.target.name;
        const value = this.state[name];
        this.setState({ [name]: !value })
    };
    getPrepProcView = () => {

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
            <div style={{marginTop:6}}>- HTML문서&nbsp;<font color={"#00b050"}>{total_html_file_count}</font>건 수집,
                추출된 텍스트 <font color={"#FF4E00"}>{total_csv_line_count}</font>줄</div>

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
                                    <td width={100}>수집 채널</td>
                                    <td width={100}>HTML 문서(건)</td>
                                    <td width={100}>추출된 텍스트(줄)</td>
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
                                    <td width={100}><font color={"#000000"}>합계</font></td>
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


        return (
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
                        <label style={{fontSize: 21, fontWeight:'bold'}}>본문 전처리</label>
                        &nbsp;&nbsp;<button onClick={this.goDetailView} style={{height: 30}}>돌아가기</button>
                    </div>
                </div>

                <hr width={"100%"} color={"#555555"}/>
                <div className="sub-title-box">
                    <div className="sub-title-outer" style={{width:'12%'}}>
                        <div className="sub-title-inner">작업명</div>
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
                        <div className="sub-title-inner">키워드</div>
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
                        <div className="sub-title-inner">수집 기간</div>
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
                        <div className="sub-title-inner">수집 채널</div>
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
                        <div className="sub-title-inner">불용어</div>
                    </div>
                    <div style={{width:10 }}/>
                    <div style={{fontSize: 14, textAlign:'left', display:'flex'}}>
                        <ul style={{lineHeight: 1.8, paddingLeft: 20}}>
                            <li>
                                <div>
                                    <button style={{
                                        fontSize:14, cursor:'pointer', height: 50, borderRadius: 5,
                                        backgroundColor:'#0099FF', color: '#FFFFFF', border:'0px'}}
                                            onClick={this.extractMorphs}>불용어 입력
                                    </button>
                                    <div style={{fontSize:12, marginTop: 5}}>- 제거할 불용어를 입력한 후 저장해주세요.</div>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>

                <div className="sub-title-box" style={{borderBottom: "1px solid #808080", marginBottom: 10}}/>
                <div className="sub-title-box">
                    <div className="sub-title-outer" style={{width:'12%'}}>
                        <div className="sub-title-inner">명사 추출</div>
                    </div>
                    <div style={{width:10 }}/>

                    <div style={{fontSize: 14, textAlign:'left', display:'flex'}}>
                        <ul style={{lineHeight: 1.8, paddingLeft: 20}}>
                            <li>
                                <div>
                                    <button style={{
                                        fontSize:14, cursor:'pointer', height: 50, borderRadius: 5,
                                        backgroundColor:'#0099FF', color: '#FFFFFF', border:'0px'}}
                                            onClick={this.extractMorphs}>명사 추출하기
                                    </button>
                                    <div style={{fontSize:12, marginTop: 5}}>- 불용어를 제거하고 명사를 추출합니다.</div>
                                </div>
                            </li>
                            <li style={{marginTop: 20}}>
                                <div style={{fontSize:16}}>명사 추출 결과</div>
                                {/*<div style={{fontSize:12}}>*/}
                                {/*    - 저장경로:<label style={{color:'#0099FF'}}>{data_directory}</label>*/}
                                {/*    &nbsp;&nbsp;<button className="open-btn" onClick={() => this.openSaveDir()}>열기</button>*/}
                                {/*</div>*/}
                                <div style={{fontSize:12}}>
                                    - 저장경로: <label style={{color:'#0099FF'}}>{data_directory + "/csv/ext.csv"}</label>
                                    &nbsp;&nbsp;<button className="open-btn" onClick={() => this.executeFile("/ext.csv")}>열기</button>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
                <div className="sub-title-box" style={{borderBottom: "1px solid #000000", marginBottom: 10}}/>
                <div className="sub-title-box" style={{marginBottom: 10}}>
                    <div className="sub-title-outer" style={{width:'12%'}}>
                        <div className="sub-title-inner">테이블 생성</div>
                    </div>
                    <div style={{width:10 }}/>
                    <div style={{fontSize: 14, textAlign:'left', display:'flex'}}>
                        <ul style={{lineHeight: 1.8, paddingLeft: 20}}>
                            <li>
                                <div style={{fontSize:16}}>테이블 선택</div>
                                <div style={{fontSize:12}}>- 생성할 테이블을 선택한 후 테이블 생성하기 버튼을 눌러주세요.</div>
                                <div style={{marginTop: 5, marginBottom: 20}}>
                                    <div style={{ textAlign: 'left', height:30, display:'flex'}}>
                                        <CheckboxTarget
                                            name={"tableTF"}
                                            style={{width:150, height:20}}
                                            text={"단어-빈도 테이블 (Term-Frequency Table; TF Table)"}
                                            checked={this.state.tableTF}
                                            onChanged={this.onTargetChanged}
                                        />
                                    </div>
                                    <div style={{ textAlign: 'left', height:30, display:'flex'}}>
                                        <CheckboxTarget
                                            name={"tableTFIDF"}
                                            style={{width:150, height:20}}
                                            text={"TF-IDF 테이블 (Term Frequency-Inverse Document Frequency Table)"}
                                            checked={this.state.tableTFIDF}
                                            onChanged={this.onTargetChanged}
                                        />
                                    </div>
                                    <div style={{ textAlign: 'left', height:30, display:'flex'}}>
                                        <CheckboxTarget
                                            name={"tableTCOO"}
                                            style={{width:150, height:20}}
                                            text={"단어 동시 출현 행렬 (Term Co-Occurrence Matrix)"}
                                            checked={this.state.tableTCOO}
                                            onChanged={this.onTargetChanged}
                                        />
                                    </div>
                                </div>
                                <button style={{
                                    fontSize:14, cursor:'pointer', height: 50, borderRadius: 5,
                                    backgroundColor:'#0099FF', color: '#FFFFFF', border:'0px'}}
                                        onClick={this.createTables}>테이블 생성하기
                                </button>
                            </li>
                            <li style={{marginTop: 20}}>
                                <div style={{fontSize:16}}>테이블 생성 결과</div>

                                <div style={{fontSize:12}}>
                                    - 단어-빈도 테이블: <label style={{color:'#0099FF'}}>{data_directory + "/csv/ext_tf_table.csv"}</label>
                                    &nbsp;&nbsp;<button className="open-btn" onClick={() => this.executeFile("ext_tf_table.csv")}>열기</button>
                                </div>
                                <div style={{fontSize:12}}>
                                    - TF-IDF 테이블: <label style={{color:'#0099FF'}}>{data_directory + "/csv/weights"}</label>
                                    &nbsp;&nbsp;<button className="open-btn" onClick={() => this.openSaveWeightsDir()}>열기</button>
                                </div>
                                <div style={{fontSize:12}}>
                                    - 단어 동시 출현 행렬: <label style={{color:'#0099FF'}}>{data_directory + "/csv/ext_coo_matrix.csv"}</label>
                                    &nbsp;&nbsp;<button className="open-btn" onClick={() => this.executeFile("ext_coo_matrix.csv")}>열기</button>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        )
    }
    getDetailView = () => {
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
                                    <td width={100}>수집 채널</td>
                                    <td width={100}>HTML 문서(건)</td>
                                    <td width={100}>추출된 텍스트(줄)</td>
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
                                    <td width={100}><font color={"#000000"}>합계</font></td>
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

        return <div style={{
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
                    <label style={{fontSize: 21, fontWeight:'bold'}}>수집 작업 상세보기</label>
                    &nbsp;&nbsp;<button onClick={this.props.prev} style={{height: 30}}>돌아가기</button>
                </div>
            </div>

            <hr width={"100%"} color={"#555555"}/>

            <div className="sub-title-box">
                <div className="sub-title-outer" style={{width:'12%'}}>
                    <div className="sub-title-inner">작업명</div>
                </div>

                <div className="contents-text-outer">
                    <div className="contents-text-inner">
                        <input style={{textAlign: 'center', fontSize: 16}} type='text' onChange={this.onNameChanged} value={this.state.item.title}/>
                        <button style={{
                            width:50, fontSize:14, cursor:'pointer', height: 36, marginLeft: 6,
                            backgroundColor:'#0099FF', color: '#FFFFFF', border:'0px'}}
                                onClick={this.updateName}>수정
                        </button>
                    </div>
                </div>
            </div>

            <div className="sub-title-box" style={{borderBottom: "1px solid #808080", marginBottom: 10}}/>

            <div className="sub-title-box">
                <div className="sub-title-outer" style={{width:'12%'}}>
                    <div className="sub-title-inner">키워드</div>
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
                    <div className="sub-title-inner">수집 기간</div>
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
                    <div className="sub-title-inner">수집 채널</div>
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
                    <div className="sub-title-inner">진행 상태</div>
                </div>
                <div style={{width:10 }}/>

                <div style={{fontSize: 14}}>
                    <ul style={{lineHeight: 2.3, paddingLeft: 20}}>
                        <li>상태: <label style={{color: R.StateExpression[this.state.item.work_state].backgroundColor}}>
                            {R.StateExpression[this.state.item.work_state].label}
                        </label>
                        </li>
                        <li>
                            수집경로: <label style={{color:'#0099FF'}}>{data_directory}</label>
                            &nbsp;&nbsp;<button className="open-btn" onClick={() => this.openSaveDir()}>열기</button>
                        </li>
                        <li>
                            수집 채널별 수집 현황
                            {collectionDetail}
                        </li>
                    </ul>
                </div>
            </div>

            <div className="sub-title-box" style={{borderBottom: "1px solid #808080", marginBottom: 10}}/>

            <div className="sub-title-box" style={{marginBottom: 10}}>
                <div className="sub-title-outer" style={{width:'12%', textAlign:"center"}}>
                    <div className="sub-title-inner">전처리 결과</div>
                    <button style={{
                        width:90, fontSize:12, cursor:'pointer', height: 30, marginTop: 130,
                        backgroundColor:'#00b050', color: '#FFFFFF', border:'0px'}}
                            onClick={this.goPreProcView}>본문 전처리
                    </button>
                </div>
                <div style={{width:10 }}/>

                <div style={{fontSize: 14, textAlign:'left', display:'flex'}}>
                    <ul style={{lineHeight: 1.8, paddingLeft: 20}}>
                        <li>
                            <div style={{fontSize:16}}>명사 추출 결과

                            </div>
                            {/*<div style={{fontSize:12, marginTop: 8}}>*/}
                            {/*    - 저장경로:<label style={{color:'#0099FF'}}>{data_directory}</label>*/}
                            {/*    &nbsp;&nbsp;<button className="open-btn" onClick={() => this.executeFile("ext_tf_table.csv")}>열기</button>*/}
                            {/*</div>*/}
                            <div style={{fontSize:12}}>- 저장경로: <label style={{color:'#0099FF'}}>{data_directory + "/csv/ext.csv"}</label>
                                &nbsp;&nbsp;<button className="open-btn" onClick={() => this.executeFile("ext.csv")}>열기</button>
                            </div>

                        </li>
                        <li style={{marginTop: 20}}>
                            <div style={{fontSize:16}}>테이블 생성 결과
                            </div>

                            <div style={{fontSize:12, marginTop: 8}}>
                                - 단어-빈도 테이블: <label style={{color:'#0099FF'}}>{data_directory + "/csv/ext_tf_table.csv"}</label>
                                &nbsp;&nbsp;<button className="open-btn" onClick={() => this.executeFile("ext_tf_table.csv")}>열기</button>
                            </div>
                            <div style={{fontSize:12}}>
                                - TF-IDF 테이블: <label style={{color:'#0099FF'}}>{data_directory + "/csv/weights"}</label>
                                &nbsp;&nbsp;<button className="open-btn" onClick={() => this.openSaveWeightsDir()}>열기</button>
                            </div>
                            <div style={{fontSize:12}}>
                                - 단어 동시 출현 행렬: <label style={{color:'#0099FF'}}>{data_directory + "/csv/ext_coo_matrix.csv"}</label>
                                &nbsp;&nbsp;<button className="open-btn" onClick={() => this.executeFile("ext_coo_matrix.csv")}>열기</button>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    }
    goPreProcView = () => { this.setState({ pageType: 1 }) }
    goDetailView = () => { this.setState({ pageType: 0 }) }

    render(){
        // alert(this.state.pageType)
        const pageType = this.state.pageType
        let view = pageType===0? this.getDetailView(): this.getPrepProcView()
        return <div>{view}</div>
    }
}

export default DetailWork;