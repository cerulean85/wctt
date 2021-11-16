import React from "react"
import '../App.css';
import * as R from "../Resources";
import cfg from "../config"
import "react-datepicker/dist/react-datepicker.css";
import axios from 'axios';
import ProgressStateTextBox from "./ProgressStateTextBox";
import WorkItem from "./WorkItem";
import {CollectTargetName} from "../Resources";

const moment = require('moment');
class PopupWorkDetail extends React.Component {

    constructor(props) {

        // console.log('constructor')
        super(props);
        this.handleMouseHover = this.handleMouseHover.bind(this);
        this.handleMouseLeave = this.handleMouseLeave.bind(this);

        this.state = {
            list: [],
            opacity: 1.0,
            item: props.item,
            log: ''
        };
        // this.textLog = React.createRef();


    }

    handleMouseHover(e) { this.setState(this.toggleHoverState); }
    handleMouseLeave(e) { this.setState(this.toggleLeaveState); }
    toggleHoverState(e) { return { opacity: 0.5 }; }
    toggleLeaveState(e) { return { opacity: 1.0 }; }

    updateName=() => {

        const request = async () => {

            // console.log('보자보자')
            // console.log(this.state.item)
            // let data = {
            //     group_id: this.state.item.group_id,
            //     name: this.state.item.name
            // };

            // console.log(data);

            // const response = await axios.post('http://localhost:3030/update_work_group_name', data);
            // if(response.status !== 200) {
            //     alert('요청한 작업을 수행할 수 없습니다.');
            // } else {
            //     alert('처리되었습니다.')
            // }
        };
        request()
    };

    onNameChanged = (d) => {
        this.state.item.name = d.target.value;
        this.setState({
            item: this.state.item,
        })
    };

    componentDidMount() {
        this.update();
        this.timerID = setInterval(
            () => this.tick(),
            1000
        );

        this.updateID = setInterval(
            () => this.update(),
            1000
        );
    }

    getWorkStateList = () => {

        // let data = {
        //     group_id: this.state.item.group_id
        // };
        //
        // axios.post('http://localhost:3030/get_work_state_list', data).then( (response) => {
        //     const list = response.data.list;
        //     this.setState({list: list});
        //     console.log(list[0])
        // });
    };

    tick() {
        this.setState({
            date: new Date()
        });

        let item = this.state.item;
        this.setState({item: item})
    }

    componentWillUnmount() {
        clearInterval(this.timerID);
        clearInterval(this.updateID);
    }

    update() {
        // axios.post(`http://${cfg.host}:${cfg.proxyPort}/action/get_work_group_list`).then( (response) => {
        //     const list = response.data.list;
        //     this.setState({list: list})
        // });
    }

    componentDidUpdate() {
        // this.textLog.current.scrollTop = this.textLog.current.scrollHeight;
    }

    onLogChanged = (d) => {
        this.state.log += '\n' + d.target.value;
        this.setState({
            log: this.state.log,
        })
    };

    renderProgressStateTextBox() {
        return <ProgressStateTextBox
            value={this.state.item.work_state}
        />;
    }

    render() {

        // let tmpKwdSet = [
        //     { keyword: this.state.item.keyword1, opt: this.state.item.keyword_opt1},
        //     { keyword: this.state.item.keyword2, opt: this.state.item.keyword_opt2},
        //     { keyword: this.state.item.keyword3, opt: this.state.item.keyword_opt3},
        //     { keyword: this.state.item.keyword4, opt: this.state.item.keyword_opt4},
        //     { keyword: this.state.item.keyword5, opt: this.state.item.keyword_opt5} ];
        //
        // let kwdKeySet = [ tmpKwdSet[0].keyword ];
        //
        // for (let i=1; i<tmpKwdSet.length; i++) {
        //
        //     const kwdKeySetSize = kwdKeySet.length;
        //     const kwdFormat = tmpKwdSet[i];
        //     if(kwdFormat.keyword === undefined || kwdFormat.keyword === '') continue;
        //
        //     if(kwdFormat.opt === 'and') {
        //         for (let k=0; k<kwdKeySetSize; k++) {
        //             const keyword = kwdKeySet[k];
        //             if(keyword === undefined || keyword === '') continue;
        //             kwdKeySet[k] = keyword + ' ' + kwdFormat.keyword;
        //         }
        //     }
        //
        //     if(kwdFormat.opt === 'or') {
        //         for (let k=0; k<kwdKeySetSize; k++) {
        //             const keyword = kwdKeySet[k];
        //             if(keyword === undefined || keyword === '') continue;
        //             kwdKeySet.push(keyword + ' ' + kwdFormat.keyword);
        //             kwdKeySet.push(kwdFormat.keyword);
        //         }
        //     }
        // }
        //
        // let keywords = '';
        // for (let i=0; i<kwdKeySet.length; i++) {
        //     keywords += kwdKeySet[i] + ( i === (kwdKeySet.length-1) ? '': '\u00A0,\u00A0\u00A0\u00A0');
        // }
        //
        let targets = '';
        const channels = this.state.item.channels.split(',');
        for(let i=0; i<channels.length; i++) {
            const name = channels[i];
            if(name === undefined || name === '') continue;
            targets += R.CollectTargetName[channels[i]] + "\u00A0\u00A0\u00A0\u00A0";
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
            <div style={{paddingTop: 7}}>&nbsp;&nbsp;HTML문서&nbsp;<font color={"#00b050"}>{total_html_file_count}</font>건 수집,
                추출된 텍스트 <font color={"#FF4E00"}>{total_csv_line_count}</font>줄</div>

        const dataDir = this.state.item.data_directory
        // eslint-disable-next-line no-unused-expressions
        let collectionDetail = <div></div>
        const currentState = this.state.item.work_state;
        if(reportArr.length > 0 && (currentState === R.STATE_ATTACHED || currentState === R.STATE_WORKING)) {



            collectionDetail =
                <div style={{
                    width: '100%',
                    marginTop: 20,
                    fontSize: 18,
                    display:'flex'
                }}>
                    <div style={{width:'20%' }}/>
                    <div style={{width: '80%', textAlign:'left'}}>
                        <div>
                            <table style={{width:500}}>
                                <tr>
                                    <td width={'25%'} style={{fontSize:16}}>수집 채널</td>
                                    <td width={'25%'} style={{fontSize:16, textAlign:'center'}}>HTML 문서(건)</td>
                                    <td width={'25%'} style={{fontSize:16, textAlign:'center'}}>추출된 텍스트(줄)</td>
                                </tr>
                            </table>
                        </div>
                        <div>
                            {
                                reportArr.map(report =>
                                    <table style={{width:500}}>
                                        <tr>
                                            <td width={'25%'}><font color={"#aaaaaa"}>{report.channelName}</font></td>
                                            <td width={'25%'} style={{textAlign:'center'}}><font color={"#00b050"}>{report.htmlFileCount}</font></td>
                                            <td width={'25%'} style={{textAlign:'center'}}><font color={"#FF4E00"}>{report.csvLineCount}</font></td>
                                        </tr>
                                    </table>
                                )
                            }
                        </div>
                    </div>
                </div>
        }

        const data_directory = this.state.item.data_directory.replaceAll("\\", "/")  + '/csv/' + this.state.item.id

        return (
            <div style={{
                position: 'fixed',
                background: '#00000044',
                width: '100%',
                height: '120vh',
                top: 0,
                left: 0
            }}>

                <div style={{
                    position: 'relative',
                    width: '80%',
                    margin: '0 auto',
                    height: 'auto',
                    maxHeight: 100,
                    marginTop: 'calc(100vh - 85vh - 20px)',
                    background: '#404040',
                    paddingTop: 10,
                    paddingBottom: 12,
                    borderTop: '1px solid #999',
                    borderLeft: '1px solid #999',
                    borderRight: '1px solid #999',
                    overflow: 'auto',
                    display: 'flex',
                    borderTopLeftRadius: 8,
                    borderTopRightRadius: 8,
                }}>
                    <div style={{fontSize: 18, color:"#FFFFFF"}}>&nbsp;&nbsp;&nbsp;&nbsp;상세 보기</div>
                    <div style={{
                        position: 'absolute',
                        width: '100%',
                        textAlign: 'right'}}>
                        <div style={{
                            cursor: 'pointer',
                            display:'inline-block',
                            width:30, height: 20,
                            paddingTop: 5, paddingRight: 14, opacity: this.state.opacity}}
                             onMouseEnter={this.handleMouseHover}
                             onMouseLeave={this.handleMouseLeave}
                             onClick={ this.props.handleClose }>
                            <img src={R.Images['close']}/>
                        </div>
                    </div>
                </div>
                <div style={{
                    position: 'relative',
                    width: '80%',
                    margin: '0 auto',
                    height: '50%',
                    background: '#FFFFFF',
                    borderLeft: '1px solid #999',
                    borderRight: '1px solid #999',
                    borderBottom: '1px solid #999',
                    overflow: 'auto',
                    borderBottomLeftRadius: 8,
                    borderBottomRightRadius: 8
                }}>
                    <div style={{
                        width: '100%',
                        marginTop: 40,
                        fontSize: 18,
                        display:'flex'
                    }}>
                        <div style={{width:'5%' }}/>
                        <div style={{width:'12%', textAlign:'center', paddingTop:8, paddingBottom:6, backgroundColor:'#dee2e6'}}>작업명</div>
                        <div style={{width:10 }}/>
                        <input style={{width: '30%', textAlign: 'center'}} type='text' onChange={this.onNameChanged} value={this.state.item.title}/>
                        <div style={{width:10 }}/>
                        <button style={{
                            width:50, fontSize:14, cursor:'pointer',
                            backgroundColor:'#0099FF', color: '#FFFFFF', border:'0px'}}
                                onClick={this.updateName}>수정
                        </button>
                    </div>
                    <div style={{
                        width: '100%',
                        marginTop: 30,
                        fontSize: 18,
                        display:'flex'
                    }}>
                        <div style={{width:'5%' }}/>
                        <div style={{width:'12%', textAlign:'center', paddingTop:8, paddingBottom:3, backgroundColor:'#dee2e6'}}>키워드</div>
                        <div style={{width:10 }}/>
                        <div style={{width:'70%', textAlign:'left', paddingTop:6, wordWrap: 'break-word', color:'#7F7F7F'}}>
                            {this.state.item.keywords}
                        </div>
                    </div>

                    <div style={{
                        width: '100%',
                        marginTop: 30,
                        fontSize: 18,
                        display:'flex'
                    }}>
                        <div style={{width:'5%' }}/>
                        <div style={{width:'12%', textAlign:'center', paddingTop:8, paddingBottom:3, backgroundColor:'#dee2e6'}}>수집기간</div>
                        <div style={{width:10 }}/>
                        <div style={{display:'flex', paddingTop:6, color:'#7F7F7F'}}>{moment(this.state.item.start_date).format('YYYY-MM-DD')}&nbsp;~&nbsp;{moment(this.state.item.end_date).format('YYYY-MM-DD')}</div>
                    </div>

                    <div style={{
                        width: '100%',
                        marginTop: 30,
                        fontSize: 18,
                        display:'flex'
                    }}>
                        <div style={{width:'5%' }}/>
                        <div style={{width:'12%', textAlign:'center', paddingTop:8, paddingBottom:3, backgroundColor:'#dee2e6'}}>수집대상</div>
                        <div style={{width:10 }}/>
                        <div style={{width:'70%', paddingTop:6, textAlign:'left', wordWrap: 'break-word', color:'#7F7F7F'}}>{targets}</div>
                    </div>

                    <div style={{
                        width: '100%',
                        marginTop: 40,
                        fontSize: 18,
                        display:'flex'
                    }}>
                        <div style={{width:'5%' }}/>
                        <div style={{width:'12%', textAlign:'center', paddingTop:8, paddingBottom:3, backgroundColor:'#dee2e6'}}>진행상태</div>
                        <div style={{width:10 }}/>
                        {this.renderProgressStateTextBox()}
                        <div style={{ color:'#7F7F7F' }}>{collectionState}</div>
                    </div>

                    <div style={{
                        width: '100%',
                        marginTop: 8,
                        fontSize: 18,
                        display:'flex'
                    }}>
                        <div style={{width:'15%' }}/>
                        <div style={{fontSize: 14, textAlign:'left', display:'flex'}}>
                            <ul style={{lineHeight: 1.8}}>
                                <li>
                                    수집경로: <label style={{color:'#0099FF'}}>{data_directory}</label>
                                </li>
                                <li>
                                    단어-빈도표: <label style={{color:'#0099FF'}}>{data_directory + "/freq_all.csv"}</label>
                                </li>
                                <li>
                                    동시출현빈도 행렬: <label style={{color:'#0099FF'}}>{data_directory + "/conc_all.csv"}</label>
                                </li>
                            </ul>
                        </div>
                    </div>

                    {collectionDetail}
                    <div style={{
                        width: '100%',
                        marginTop: 40,
                        fontSize: 18,
                        display:'flex'
                    }}>
                        <div style={{width:'5%' }}/>
                        <div style={{width:'12%', textAlign:'center', paddingTop:8, paddingBottom:3, backgroundColor:'#dee2e6'}}>시각화</div>

                    </div>

                    <div style={{width:'20%', paddingTop:5, textAlign: "left", marginLeft: 20 }}>
                        <ul><li>워드클라우드</li></ul>
                    </div>
                    <div style={{float:"left", textAlign: "center", width: "100%", height: 400}}>
                        <img height={"400"}
                             src={process.env.PUBLIC_URL + "\\wordcloud\\" + this.state.item.id + "\\wc_all.png"}/>
                    </div>
                </div>
            </div>

        );
    }
}
export default PopupWorkDetail;
