//mail
import React, { Component } from "react";
import ButtonOpenAddWorkWindow from "./components/ButtonOpenAddWorkWindow"
import WorkTable from "./components/WorkTable"
import PopupWorkCreate from "./components/PopupWorkCreate"
import axios from "axios";
import cfg from "./config";
import moment from "moment";
import DatePicker, {registerLocale} from "react-datepicker";
import ko from 'date-fns/locale/ko';
import CheckboxTarget from "./components/CheckboxTarget";
import ButtonControlPopup from "./components/ButtonCreateWork";
import styled from "styled-components";
registerLocale('ko', ko)

const ParentComponent = props => (
    <div>
        <div style={{
            width: '100%',
            marginTop: 20,
            fontSize: 18,
            display:'flex',
        }}>
            <div style={{width:'5%' }}/>
            <div style={{width:'10%', textAlign:'center', paddingTop:8, backgroundColor:'#dee2e6'}}>키워드1</div>
            <div style={{width:10 }}/>
            <input style={{width: '200', fontSize: 18, textAlign: "center"}} type='text' onChange={props.keywordChanged} value={props.keyword1}/>
            <div style={{width:10 }}/>

            <button style={{
                width:50, fontSize:14, cursor:'pointer',
                backgroundColor:'#0099FF', color: '#FFFFFF', border:'0px'}}
                    onClick={props.addChild}>추가
            </button>

        </div>
        <div>
            {props.children}
        </div>
    </div>
);

const ChildComponent = (props) => <div>
    <div style={{
        width: '100%',
        marginTop: 20,
        fontSize: 18,
        display:'flex'
    }}>
        <div style={{width:'5%' }}/>
        <div style={{width:'10%', textAlign:'center', paddingTop:8, backgroundColor:'#dee2e6'}}>키워드{props.number}</div>
        <div style={{width:10 }}/>
        <input style={{width: '220', fontSize: 18, textAlign: "center"}} type='text'
               onChange={props.keywordChanged}
               value={props.keyword} />
    </div>
</div>;

class Collection extends React.Component{
    constructor(props) {
        super(props);
        this.handleMouseHover = this.handleMouseHover.bind(this);
        this.handleMouseLeave = this.handleMouseLeave.bind(this);
        this.state = {
            opacity: 1.0,
            numChildren: 1,
            name: '테스트',
            keyword1: '코로나 백신',
            keywordOpt1: 'and',
            startDate: '', //moment('2021-02-26').toDate(),
            endDate: '', //moment('2021-10-31').toDate(),
            targetNaver: false,
            targetDaum: false,
            targetChosun: false,
            targetDonga: false,
            targetJoongang: false,
            targetTweeter: false,
            targetFacebook: false,
            targetNaverBlog: false,
            targetInstagram: false,
            data_directory: ''
        };
    }

    componentDidMount() {
        axios.post(`http://${cfg.host}:${cfg.proxyPort}/action/get_data_directory`).then( (response) => {
            const data_directory = response.data.data_directory;
            this.setState({data_directory: data_directory})
        });
    }

    handleMouseHover(e) { this.setState(this.toggleHoverState); }
    handleMouseLeave(e) { this.setState(this.toggleLeaveState); }
    toggleHoverState(e) { return { opacity: 0.5 }; }
    toggleLeaveState(e) { return { opacity: 1.0 }; }

    onAddChild = () => {
        if( this.state.numChildren === 5) {
            alert('더 이상 키워드를 추가할 수 없습니다.');
            return;
        }

        this.state[ 'keyword' + ( this.state.numChildren + 1 )  ] = '';
        this.setState({
            numChildren: this.state.numChildren + 1
        });
    };

    onNameChanged = (d) => {
        // console.log(d)
        this.setState({
            name: d.target.value,
        })
    };

    onStartDateChanged = (d) => {
        this.setState({
            startDate: d,
        })
    };

    onEndDateChanged = (d) => {
        this.setState({
            endDate: d,
        })
    };

    onTargetChanged = (d) => {
        const name = d.target.name;
        const value = this.state[name];
        this.setState({ [name]: !value })
    };

    onSubmit = (e) => {
        let collectTarget = (
            // (this.state.targetNaver === true ? 'naver/' : '') +
            // (this.state.targetDaum === true ? 'daum/' : '') +
            // (this.state.targetChosun === true ? 'chosun/' : '') +
            (this.state.targetJoongang === true ? 'jna,' : '') +
            (this.state.targetDonga === true ? 'dna,' : '') +
            (this.state.targetTweeter === true ? 'twt,' : '') +
            (this.state.targetInstagram === true ? 'ins,' : '') +
            (this.state.targetNaverBlog === true ? 'nav,' : '')
        );

        let data = {
            title: this.state.name,
            start_dt: moment(this.state.startDate).format('YYYY-MM-DD'),
            end_dt: moment(this.state.endDate).format('YYYY-MM-DD'),
            channels: collectTarget,
            keywords: '',
            key_opts: '',
            data_directory: this.state.data_directory
        };

        data['keywords'] = ''
        for(let i=0; i<this.state.numChildren; i++) {
            const no = (i + 1);
            data['keywords'] += this.state['keyword' + no]  + ',';
        }

        if (data['channels'].length > 0)
            data['channels'] = data['channels'].substr(0, data['channels'].length - 1)

        if (data['keywords'].length > 0)
            data['keywords'] = data['keywords'].substr(0, data['keywords'].length - 1)

        if(window.confirm('새 작업을 추가하시겠습니까?')) {

            axios.post(`http://${cfg.host}:${cfg.proxyPort}/action/enroll_works`, data).then((response) => {
                console.log(data)
                if(response.status === 200) {
                    window.location.reload();
                    window.scrollTo(0, 0);
                }
            });
        }
    };

    render(){

        const DTPicker = styled(DatePicker)`font-size:18px;text-align: center`

        const childrenNums = [];
        for (var i = 2; i < this.state.numChildren + 1; i += 1) {
            childrenNums.push(i);
        }
        const listItems = childrenNums.map((no) =>
            <ChildComponent key={no} number={no}
                            name={'keyword' + no}
                            keywordChanged={(e) => {
                                this.setState({['keyword' + no] : e.target.value})
                            }}
                            keyword={this.state['keyword' + no]}/>
        );

        return (
            <div className="App">
                <div style={{
                    marginTop: 20,
                    marginLeft: 30,
                    marginBottom: 40,
                    color: "#1F1F1F",
                    textAlign: "left"
                }}>
                    <h2>Create a new task</h2>
                    <h4>&nbsp;&nbsp;※ 새로운 수집 작업을 등록해주세요.</h4>
                    <hr width={"100%"} color={"#555555"}/>
                </div>

                <div style={{
                    width: '100%',
                    marginTop: 30,
                    fontSize: 18,
                    display:'flex'
                }}>
                    <div style={{width:'5%' }}/>
                    <div style={{paddingTop:8, width:'10%', backgroundColor:'#dee2e6', textAlign:'center'}}>작업 이름</div>
                    <div style={{width:10 }}/>
                    <input style={{width: 220, fontSize: 18, textAlign: "center"}} type='text' onChange={this.onNameChanged} value={this.state.name}/>
                    <div style={{width:'5%' }}/>
                </div>

                <ParentComponent
                    addChild={this.onAddChild}
                    keywordChanged={(e) => {
                        this.setState({
                            keyword1: e.target.value,
                        })
                    }}
                    keywordOptChanged={(e) => {
                        this.setState({
                            keywordOpt1: e.target.value,
                        })
                    }}
                    keyword1={this.state.keyword1}
                    keywordOpt1={this.state.keywordOpt1}>
                    {listItems}
                </ParentComponent>

                <div style={{
                    width: '100%',
                    marginTop: 20,
                    fontSize: 18,
                    display:'flex'
                }}>
                    <div style={{width:'5%' }}/>
                    <div style={{width:'10%', textAlign:'center', paddingTop:8, backgroundColor:'#dee2e6'}}>수집 기간</div>
                    <div style={{width:10 }}/>
                    <DTPicker style={{width:100, textAlign:'center'}}
                              onChange={this.onStartDateChanged}
                              selected={this.state.startDate}
                              locale={ko}
                              dateFormat="시작일: yyyy-MM-dd"/>
                    <div style={{width:'1%' }}/>
                    <div style={{paddingTop:8}}>-</div>
                    <div style={{width:'1%' }}/>
                    <DTPicker style={{width:100, textAlign:'center'}}
                              name='endDate'
                              onChange={this.onEndDateChanged}
                              selected={this.state.endDate}
                              locale={ko}
                              dateFormat="종료일: yyyy-MM-dd"/>
                </div>

                <div style={{
                    width: '100%',
                    marginTop: 20,
                    fontSize: 18,
                    display:'flex'
                }}>
                    <div style={{width:'5%' }}/>
                    <div style={{width:'10%', textAlign:'center', paddingTop:8, paddingBottom:6, backgroundColor:'#dee2e6'}}>수집채널</div>
                    <div style={{width:'3%' }}/>
                    <div style={{width: '80%', display:'flex'}}>
                        <CheckboxTarget
                            name={"targetNaverBlog"}
                            width={150}
                            text={"네이버 블로그"}
                            checked={this.state.targetNaverBlog}
                            onChanged={this.onTargetChanged}
                        />
                        <div style={{width:25 }}/>
                        <CheckboxTarget
                            name={"targetTweeter"}
                            width={100}
                            text={"트위터"}
                            checked={this.state.targetTweeter}
                            onChanged={this.onTargetChanged}
                        />
                        <div style={{width:50 }}/>
                        <CheckboxTarget
                            name={"targetInstagram"}
                            width={120}
                            text={"인스타그램"}
                            checked={this.state.targetInstagram}
                            onChanged={this.onTargetChanged}
                        />
                    </div>
                </div>
                <div style={{
                    width: '100%',
                    marginTop: 20,
                    fontSize: 18,
                    display:'flex'
                }}>
                    <div style={{width:'18%', textAlign:'center'}} />
                    <div style={{width: '80%', display:'flex'}}>
                        <CheckboxTarget
                            name={"targetDonga"}
                            width={125}
                            text={"동아일보"}
                            checked={this.state.targetTweeter}
                            onChanged={this.onTargetChanged}
                        />
                        <div style={{width:50 }}/>
                        <CheckboxTarget
                            name={"targetJoongang"}
                            width={100}
                            text={"중앙일보"}
                            checked={this.state.targetTweeter}
                            onChanged={this.onTargetChanged}
                        />
                    </div>
                </div>

                <div style={{textAlign: 'center', borderBottom: '1px solid #000000', marginLeft: 30}}>
                    <ButtonControlPopup width={120} height={40} backgroundColor={'#0099FF'} onClick={this.onSubmit} text={'등록하기'} style={{marginBottom:30}}/>
                    <ButtonControlPopup width={80} height={40} backgroundColor={'#ACACAC'} onClick={this.props.handleClose} text={'초기화'} marginLeft={20} />
                    <div style={{height:30}}></div>
                </div>


                <div className="App">
                    <div style={{
                        marginTop: 60,
                        marginLeft: 30,
                        color: "#1F1F1F",
                        textAlign: "left"
                    }}>
                        <h2>Task List</h2>
                        <h4>&nbsp;&nbsp;※ 등록된 수집 작업 목록을 확인할 수 있습니다.</h4>
                        <hr width={"100%"} color={"#555555"}/>
                    </div>

                    <WorkTable openPopup={this.togglePopup}/>
                    {this.state.isOpen && <PopupWorkCreate
                        content={<>
                        </>}
                        handleClose={this.togglePopup}
                    />}
                </div>


            </div>
        );
    }
}

export default Collection;