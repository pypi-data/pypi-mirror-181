//ϵͳ
#ifdef WIN32
//#include "stdafx.h"
#endif

#include "vnemt.h"
#include "pybind11/pybind11.h"
#include "emt/emt_trader_api.h"


using namespace pybind11;
using namespace EMT::API;


///-------------------------------------------------------------------------------------
///C++ SPI�Ļص���������ʵ��
///-------------------------------------------------------------------------------------

//API�ļ̳�ʵ��
class TdApi : public TraderSpi
{
private:
	TraderApi* api = NULL;            //API����
	bool active = false;       //����״̬

public:
	TdApi()
	{
	};

	~TdApi()
	{
		if (this->active)
		{
			this->exit();
		}
	};

	//-------------------------------------------------------------------------------------
	//API�ص�����
	//-------------------------------------------------------------------------------------

    ///���ӳɹ�֪ͨ
            ///@remark ���ͻ����뽻�׺�̨�ɹ���������ʱ���÷��������ã�OnConnected�ӿڽ��������ӳɹ�֪ͨ����Ҫ���ٷ��أ��û������ڴ˺����������⴦��
    virtual void OnConnected();

    ///����֪ͨ
    ///@param reason ����ԭ��������������Ӧ
    ///@remark ���ͻ����뽻�׺�̨��ͨ�����ӶϿ�ʱ���÷��������ã�api�ڲ�֧���Զ��������ƣ�OnDisconnected�ӿڽ���������֪ͨ����Ҫ���ٷ��أ��û������ڴ˺����������⴦��
    virtual void OnDisconnected(int reason);

    ///����Ӧ��
    ///@param error_info ����������Ӧ��������ʱ�ľ���Ĵ������ʹ�����Ϣ,��error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@remark �˺���ֻ���ڷ�������������ʱ�Ż���ã�һ�������û�����
    virtual void OnError(EMTRI* error_info);

    ///����֪ͨ
    ///@param order_info ������Ӧ������Ϣ���û�����ͨ��order_info.order_emt_id����������ͨ��GetClientIDByEMTID() == client_id�������Լ��Ķ�����order_info.qty_left�ֶ��ڶ���Ϊδ�ɽ������ɡ�ȫ�ɡ��ϵ�״̬ʱ����ʾ�˶�����û�гɽ����������ڲ�����ȫ��״̬ʱ����ʾ�˶���������������order_info.order_cancel_emt_idΪ������Ӧ�ĳ���ID����Ϊ0ʱ��ʾ�˵������ɹ�
    ///@param error_info �������ܾ����߷�������ʱ�������ʹ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ÿ�ζ���״̬����ʱ�����ᱻ���ã���Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߣ��ڶ���δ�ɽ���ȫ���ɽ���ȫ�����������ֳ������Ѿܾ���Щ״̬ʱ������Ӧ�����ڲ��ֳɽ�����������ɶ����ĳɽ��ر�������ȷ�ϡ����е�¼�˴��û��Ŀͻ��˶����յ����û��Ķ�����Ӧ
    virtual void OnOrderEvent(EMTOrderInfo* order_info, EMTRI* error_info, uint64_t session_id);

    ///�ɽ�֪ͨ
    ///@param trade_info �ɽ��ر��ľ�����Ϣ���û�����ͨ��trade_info.order_emt_id����������ͨ��GetClientIDByEMTID() == client_id�������Լ��Ķ����������Ͻ�����exec_id����Ψһ��ʶһ�ʳɽ���������2�ʳɽ��ر�ӵ����ͬ��exec_id���������Ϊ�˱ʽ����Գɽ��ˡ����������exec_id��Ψһ�ģ���ʱ�޴��жϻ��ơ�report_index+market�ֶο������Ψһ��ʶ��ʾ�ɽ��ر���
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark �����гɽ�������ʱ�򣬻ᱻ���ã���Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ����е�¼�˴��û��Ŀͻ��˶����յ����û��ĳɽ��ر�����ض���Ϊ����״̬����Ҫ�û�ͨ���ɽ��ر��ĳɽ�������ȷ����OnOrderEvent()�������Ͳ���״̬��
    virtual void OnTradeEvent(EMTTradeReport* trade_info, uint64_t session_id);

    ///����������Ӧ
    ///@param cancel_info ����������Ϣ������������order_cancel_emt_id�ʹ�������order_emt_id
    ///@param error_info �������ܾ����߷�������ʱ�������ʹ�����Ϣ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߣ���error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ����Ӧֻ���ڳ�����������ʱ���ص�
    virtual void OnCancelOrderError(EMTOrderCancelInfo* cancel_info, EMTRI* error_info, uint64_t session_id);

    ///�����ѯ������Ӧ
    ///@param order_info ��ѯ����һ������
    ///@param error_info ��ѯ����ʱ��������ʱ�����صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ����֧�ַ�ʱ�β�ѯ��һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    virtual void OnQueryOrder(EMTQueryOrderRsp* order_info, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///��ҳ�����ѯ������Ӧ
    ///@param order_info ��ѯ����һ������
    ///@param req_count ���󵽵��������
    ///@param order_sequence ��ҳ����ĵ�ǰ�ر�����
    ///@param query_reference ��ǰ������Ϣ����Ӧ�Ĳ�ѯ��������Ҫ��¼�������ڽ�����һ�η�ҳ��ѯ��ʱ����Ҫ�õ�
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��order_sequenceΪ0���������β�ѯû�в鵽�κμ�¼����is_lastΪtrueʱ�����order_sequence����req_count����ô��ʾ���б��������Խ�����һ�η�ҳ��ѯ��������ȣ���ʾ���б����Ѿ���ѯ��ϡ�һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ�
    virtual void OnQueryOrderByPage(EMTQueryOrderRsp* order_info, int64_t req_count, int64_t order_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id);

    ///�����ѯ�ɽ���Ӧ
    ///@param trade_info ��ѯ����һ���ɽ��ر�
    ///@param error_info ��ѯ�ɽ��ر���������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ����֧�ַ�ʱ�β�ѯ��һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    virtual void OnQueryTrade(EMTQueryTradeRsp* trade_info, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///��ҳ�����ѯ�ɽ���Ӧ
    ///@param trade_info ��ѯ����һ���ɽ���Ϣ
    ///@param req_count ���󵽵��������
    ///@param trade_sequence ��ҳ����ĵ�ǰ�ر�����
    ///@param query_reference ��ǰ������Ϣ����Ӧ�Ĳ�ѯ��������Ҫ��¼�������ڽ�����һ�η�ҳ��ѯ��ʱ����Ҫ�õ�
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��trade_sequenceΪ0���������β�ѯû�в鵽�κμ�¼����is_lastΪtrueʱ�����trade_sequence����req_count����ô��ʾ���лر������Խ�����һ�η�ҳ��ѯ��������ȣ���ʾ���лر��Ѿ���ѯ��ϡ�һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ�
    virtual void OnQueryTradeByPage(EMTQueryTradeRsp* trade_info, int64_t req_count, int64_t trade_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id);

    ///�����ѯͶ���ֲ߳���Ӧ
    ///@param position ��ѯ����һֻ��Ʊ�ĳֲ����
    ///@param error_info ��ѯ�˻��ֲַ�������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark �����û����ܳ��ж����Ʊ��һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    virtual void OnQueryPosition(EMTQueryStkPositionRsp* position, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///��ҳ�����ѯ�ֲ���Ӧ
    ///@param trade_info ��ѯ����һ���ֲ���Ϣ
    ///@param req_count ���󵽵��������
    ///@param trade_sequence ��ҳ����ĵ�ǰ�ر�����
    ///@param query_reference ��ǰ������Ϣ����Ӧ�Ĳ�ѯ��������Ҫ��¼�������ڽ�����һ�η�ҳ��ѯ��ʱ����Ҫ�õ�
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��trade_sequenceΪ0���������β�ѯû�в鵽�κμ�¼����is_lastΪtrueʱ�����trade_sequence����req_count����ô��ʾ���лر������Խ�����һ�η�ҳ��ѯ��������ȣ���ʾ���лر��Ѿ���ѯ��ϡ�һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ�
    virtual void OnQueryPositionByPage(EMTQueryStkPositionRsp* trade_info, int64_t req_count, int64_t trade_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id);

    ///�����ѯ�ʽ��˻���Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    ///@param asset ��ѯ�����ʽ��˻����
    ///@param error_info ��ѯ�ʽ��˻���������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    virtual void OnQueryAsset(EMTQueryAssetRsp* asset, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///�����ѯ�ʽ𻮲�������Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    ///@param fund_transfer_info ��ѯ�����ʽ��˻����
    ///@param error_info ��ѯ�ʽ��˻���������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    virtual void OnQueryFundTransfer(EMTFundTransferNotice* fund_transfer_info, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///�ʽ𻮲�֪ͨ
    ///@param fund_transfer_info �ʽ𻮲�֪ͨ�ľ�����Ϣ���û�����ͨ��fund_transfer_info.serial_id����������ͨ��GetClientIDByEMTID() == client_id�������Լ��Ķ�����
    ///@param error_info �ʽ𻮲��������ܾ����߷�������ʱ�������ʹ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д��󡣵��ʽ𻮲�����Ϊһ�������Ľڵ�֮�仮������error_info.error_id=11000384ʱ��error_info.error_msgΪ����п����ڻ������ʽ�������Ϊ׼�����û������stringToInt��ת�����ɾݴ���д���ʵ��ʽ��ٴη��𻮲�����
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ���ʽ𻮲�������״̬�仯��ʱ�򣬻ᱻ���ã���Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ����е�¼�˴��û��Ŀͻ��˶����յ����û����ʽ𻮲�֪ͨ��
    virtual void OnFundTransfer(EMTFundTransferNotice* fund_transfer_info, EMTRI* error_info, uint64_t session_id);

    ///�����ѯ�����ڵ�����ʽ����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    ///@param fund_info ��ѯ���������ڵ�����ʽ����
    ///@param error_info ��ѯ�����ڵ�����ʽ�������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    virtual void OnQueryOtherServerFund(EMTFundQueryRsp* fund_info, EMTRI* error_info, int request_id, uint64_t session_id);

    ///�����ѯETF�嵥�ļ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    ///@param etf_info ��ѯ����ETF�嵥�ļ����
    ///@param error_info ��ѯETF�嵥�ļ���������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    virtual void OnQueryETF(EMTQueryETFBaseRsp* etf_info, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///�����ѯETF��Ʊ������Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    ///@param etf_component_info ��ѯ����ETF��Լ����سɷֹ���Ϣ
    ///@param error_info ��ѯETF��Ʊ����������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    virtual void OnQueryETFBasket(EMTQueryETFComponentRsp* etf_component_info, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///�����ѯ�����¹��깺��Ϣ�б����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    ///@param ipo_info ��ѯ���Ľ����¹��깺��һֻ��Ʊ��Ϣ
    ///@param error_info ��ѯ�����¹��깺��Ϣ�б�������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    virtual void OnQueryIPOInfoList(EMTQueryIPOTickerRsp* ipo_info, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///�����ѯ�û��¹��깺�����Ϣ����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    ///@param quota_info ��ѯ�����û�ĳ���г��Ľ����¹��깺�����Ϣ
    ///@param error_info ���ѯ�û��¹��깺�����Ϣ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    virtual void OnQueryIPOQuotaInfo(EMTQueryIPOQuotaRsp* quota_info, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///�����ѯ��Ȩ��Լ����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    ///@param option_info ��ѯ������Ȩ��Լ���
    ///@param error_info ��ѯ��Ȩ��Լ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    virtual void OnQueryOptionAuctionInfo(EMTQueryOptionAuctionInfoRsp* option_info, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///������ȯҵ�����ֽ�ֱ�ӻ������Ӧ
    ///@param cash_repay_info �ֽ�ֱ�ӻ���֪ͨ�ľ�����Ϣ���û�����ͨ��cash_repay_info.emt_id����������ͨ��GetClientIDByEMTID() == client_id�������Լ��Ķ�����
    ///@param error_info �ֽ𻹿������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    virtual void OnCreditCashRepay(EMTCrdCashRepayRsp* cash_repay_info, EMTRI* error_info, uint64_t session_id);

    ///������ȯҵ�����ֽ�Ϣ����Ӧ
    ///@param cash_repay_info �ֽ�Ϣ֪ͨ�ľ�����Ϣ���û�����ͨ��cash_repay_info.emt_id����������ͨ��GetClientIDByEMTID() == client_id�������Լ��Ķ�����
    ///@param error_info �ֽ�Ϣ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    virtual void OnCreditCashRepayDebtInterestFee(EMTCrdCashRepayDebtInterestFeeRsp* cash_repay_info, EMTRI* error_info, uint64_t session_id);

    ///�����ѯ������ȯҵ���е��ֽ�ֱ�ӻ��������Ӧ
    ///@param cash_repay_info ��ѯ����ĳһ���ֽ�ֱ�ӻ���֪ͨ�ľ�����Ϣ
    ///@param error_info ��ѯ�ֽ�ֱ�ӱ�����������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    virtual void OnQueryCreditCashRepayInfo(EMTCrdCashRepayInfo* cash_repay_info, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///�����ѯ�����˻�������Ϣ����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    ///@param fund_info ��ѯ���������˻�������Ϣ���
    ///@param error_info ��ѯ�����˻�������Ϣ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    virtual void OnQueryCreditFundInfo(EMTCrdFundInfo* fund_info, EMTRI* error_info, int request_id, uint64_t session_id);

    ///�����ѯ�����˻���ծ��Ϣ����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    ///@param debt_info ��ѯ���������˻���Լ��ծ���
    ///@param error_info ��ѯ�����˻���ծ��Ϣ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    virtual void OnQueryCreditDebtInfo(EMTCrdDebtInfo* debt_info, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///��ҳ�����ѯ��ծ��Ϣ��Ӧ
    ///@param debt_info ��ѯ����һ����ծ��Ϣ
    ///@param req_count ���󵽵��������
    ///@param order_sequence ��ҳ����ĵ�ǰ�ر�����
    ///@param query_reference ��ǰ��ծ��Ϣ��Ϣ����Ӧ�Ĳ�ѯ��������Ҫ��¼�������ڽ�����һ�η�ҳ��ѯ��ʱ����Ҫ�õ�
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��order_sequenceΪ0���������β�ѯû�в鵽�κμ�¼����is_lastΪtrueʱ�����order_sequence����req_count����ô��ʾ���и�ծ��Ϣ�����Խ�����һ�η�ҳ��ѯ��������ȣ���ʾ���и�ծ��Ϣ�Ѿ���ѯ��ϡ�һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ�
    virtual void OnQueryCreditDebtInfoByPage(EMTCrdDebtInfo* debt_info, int64_t req_count, int64_t order_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id);

    ///�����ѯ�����˻�ָ��֤ȯ��ծδ����Ϣ��Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    ///@param debt_info ��ѯ���������˻�ָ��֤ȯ��ծδ����Ϣ���
    ///@param error_info ��ѯ�����˻�ָ��֤ȯ��ծδ����Ϣ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    virtual void OnQueryCreditTickerDebtInfo(EMTCrdDebtStockInfo* debt_info, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///�����ѯ�����˻������ʽ����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    ///@param remain_amount ��ѯ���������˻������ʽ�
    ///@param error_info ��ѯ�����˻������ʽ�������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    virtual void OnQueryCreditAssetDebtInfo(double remain_amount, EMTRI* error_info, int request_id, uint64_t session_id);

    ///�����ѯ�����˻�����ȯͷ����Ϣ����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    ///@param assign_info ��ѯ���������˻�����ȯͷ����Ϣ
    ///@param error_info ��ѯ�����˻�����ȯͷ����Ϣ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    virtual void OnQueryCreditTickerAssignInfo(EMTClientQueryCrdPositionStkInfo* assign_info, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///��ҳ�����ѯ֤ȯͷ����Ϣ��Ӧ
    ///@param debt_info ��ѯ����һ��֤ȯͷ����Ϣ
    ///@param req_count ���󵽵��������
    ///@param order_sequence ��ҳ����ĵ�ǰ�ر�����
    ///@param query_reference ��ǰ֤ȯͷ����Ϣ��Ϣ����Ӧ�Ĳ�ѯ��������Ҫ��¼�������ڽ�����һ�η�ҳ��ѯ��ʱ����Ҫ�õ�
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��order_sequenceΪ0���������β�ѯû�в鵽�κμ�¼����is_lastΪtrueʱ�����order_sequence����req_count����ô��ʾ����֤ȯͷ����Ϣ�����Խ�����һ�η�ҳ��ѯ��������ȣ���ʾ����֤ȯͷ����Ϣ�Ѿ���ѯ��ϡ�һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ�
    virtual void OnQueryCreditTickerAssignInfoByPage(EMTClientQueryCrdPositionStkInfo* debt_info, int64_t req_count, int64_t order_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id);

    ///������ȯҵ���������ѯָ����ȯ��Ϣ����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    ///@param stock_info ��ѯ������ȯ��Ϣ
    ///@param error_info ��ѯ�����˻���ȯ��Ϣ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    virtual void OnQueryCreditExcessStock(EMTClientQueryCrdSurplusStkRspInfo* stock_info, EMTRI* error_info, int request_id, uint64_t session_id);

    ///������ȯҵ���������ѯ��ȯ��Ϣ����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    ///@param stock_info ��ѯ������ȯ��Ϣ
    ///@param error_info ��ѯ�����˻���ȯ��Ϣ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    virtual void OnQueryMulCreditExcessStock(EMTClientQueryCrdSurplusStkRspInfo* stock_info, EMTRI* error_info, int request_id, uint64_t session_id, bool is_last);

    ///������ȯҵ���и�ծ��Լչ�ڵ�֪ͨ
    ///@param debt_extend_info ��ծ��Լչ��֪ͨ�ľ�����Ϣ���û�����ͨ��debt_extend_info.emtid����������ͨ��GetClientIDByEMTID() == client_id�������Լ��Ķ�����
    ///@param error_info ��ծ��Լչ�ڶ������ܾ����߷�������ʱ�������ʹ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ����ծ��Լչ�ڶ�����״̬�仯��ʱ�򣬻ᱻ���ã���Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ����е�¼�˴��û��Ŀͻ��˶����յ����û��ĸ�ծ��Լչ��֪ͨ��
    virtual void OnCreditExtendDebtDate(EMTCreditDebtExtendNotice* debt_extend_info, EMTRI* error_info, uint64_t session_id);

    ///��ѯ������ȯҵ���и�ծ��Լչ�ڶ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    ///@param debt_extend_info ��ѯ���ĸ�ծ��Լչ�����
    ///@param error_info ��ѯ��ծ��Լչ�ڷ�������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д��󡣵�error_info.error_id=11000350ʱ������û�м�¼����Ϊ������0ֵʱ��������Լ�����ܵ�ʱ�Ĵ���ԭ��
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    virtual void OnQueryCreditExtendDebtDateOrders(EMTCreditDebtExtendNotice* debt_extend_info, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///��ѯ������ȯҵ���������˻�������Ϣ����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    ///@param fund_info �����˻�������Ϣ
    ///@param error_info ��ѯ�����˻�������Ϣ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    virtual void OnQueryCreditFundExtraInfo(EMTCrdFundExtraInfo* fund_info, EMTRI* error_info, int request_id, uint64_t session_id);

    ///��ѯ������ȯҵ���������˻�ָ��֤ȯ�ĸ�����Ϣ����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    ///@param fund_info �����˻�ָ��֤ȯ�ĸ�����Ϣ
    ///@param error_info ��ѯ�����˻�������Ϣ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    virtual void OnQueryCreditPositionExtraInfo(EMTCrdPositionExtraInfo* fund_info, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///��Ȩ��ϲ��Ա���֪ͨ
    ///@param order_info ������Ӧ������Ϣ���û�����ͨ��order_info.order_emt_id����������ͨ��GetClientIDByEMTID() == client_id�������Լ��Ķ�����order_info.qty_left�ֶ��ڶ���Ϊδ�ɽ������ɡ�ȫ�ɡ��ϵ�״̬ʱ����ʾ�˶�����û�гɽ����������ڲ�����ȫ��״̬ʱ����ʾ�˶���������������order_info.order_cancel_emt_idΪ������Ӧ�ĳ���ID����Ϊ0ʱ��ʾ�˵������ɹ�
    ///@param error_info �������ܾ����߷�������ʱ�������ʹ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ÿ�ζ���״̬����ʱ�����ᱻ���ã���Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߣ��ڶ���δ�ɽ���ȫ���ɽ���ȫ�����������ֳ������Ѿܾ���Щ״̬ʱ������Ӧ�����ڲ��ֳɽ�����������ɶ����ĳɽ��ر�������ȷ�ϡ����е�¼�˴��û��Ŀͻ��˶����յ����û��Ķ�����Ӧ
    virtual void OnOptionCombinedOrderEvent(EMTOptCombOrderInfo* order_info, EMTRI* error_info, uint64_t session_id);

    ///��Ȩ��ϲ��Գɽ�֪ͨ
    ///@param trade_info �ɽ��ر��ľ�����Ϣ���û�����ͨ��trade_info.order_emt_id����������ͨ��GetClientIDByEMTID() == client_id�������Լ��Ķ����������Ͻ�����exec_id����Ψһ��ʶһ�ʳɽ���������2�ʳɽ��ر�ӵ����ͬ��exec_id���������Ϊ�˱ʽ����Գɽ��ˡ����������exec_id��Ψһ�ģ���ʱ�޴��жϻ��ơ�report_index+market�ֶο������Ψһ��ʶ��ʾ�ɽ��ر���
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark �����гɽ�������ʱ�򣬻ᱻ���ã���Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ����е�¼�˴��û��Ŀͻ��˶����յ����û��ĳɽ��ر�����ض���Ϊ����״̬����Ҫ�û�ͨ���ɽ��ر��ĳɽ�������ȷ����OnOrderEvent()�������Ͳ���״̬��
    virtual void OnOptionCombinedTradeEvent(EMTOptCombTradeReport* trade_info, uint64_t session_id);

    ///��Ȩ��ϲ��Գ���������Ӧ
    ///@param cancel_info ����������Ϣ������������order_cancel_emt_id�ʹ�������order_emt_id
    ///@param error_info �������ܾ����߷�������ʱ�������ʹ�����Ϣ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߣ���error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ����Ӧֻ���ڳ�����������ʱ���ص�
    virtual void OnCancelOptionCombinedOrderError(EMTOptCombOrderCancelInfo* cancel_info, EMTRI* error_info, uint64_t session_id);

    ///�����ѯ��Ȩ��ϲ��Ա�����Ӧ
    ///@param order_info ��ѯ����һ������
    ///@param error_info ��ѯ����ʱ��������ʱ�����صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ����֧�ַ�ʱ�β�ѯ��һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ��˶�Ӧ����������������ѯʹ�ã�������������ʱ����������û���·ӵ�£�����api����
    virtual void OnQueryOptionCombinedOrders(EMTQueryOptCombOrderRsp* order_info, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///��ҳ�����ѯ��Ȩ��ϲ��Ա�����Ӧ
    ///@param order_info ��ѯ����һ������
    ///@param req_count ���󵽵��������
    ///@param order_sequence ��ҳ����ĵ�ǰ�ر�����
    ///@param query_reference ��ǰ������Ϣ����Ӧ�Ĳ�ѯ��������Ҫ��¼�������ڽ�����һ�η�ҳ��ѯ��ʱ����Ҫ�õ�
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��order_sequenceΪ0���������β�ѯû�в鵽�κμ�¼����is_lastΪtrueʱ�����order_sequence����req_count����ô��ʾ���б��������Խ�����һ�η�ҳ��ѯ��������ȣ���ʾ���б����Ѿ���ѯ��ϡ�һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ�
    virtual void OnQueryOptionCombinedOrdersByPage(EMTQueryOptCombOrderRsp* order_info, int64_t req_count, int64_t order_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id);

    ///�����ѯ��Ȩ��ϲ��Գɽ���Ӧ
    ///@param trade_info ��ѯ����һ���ɽ��ر�
    ///@param error_info ��ѯ�ɽ��ر���������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ����֧�ַ�ʱ�β�ѯ��һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ��˶�Ӧ����������������ѯʹ�ã�������������ʱ����������û���·ӵ�£�����api����
    virtual void OnQueryOptionCombinedTrades(EMTQueryOptCombTradeRsp* trade_info, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///��ҳ�����ѯ��Ȩ��ϲ��Գɽ���Ӧ
    ///@param trade_info ��ѯ����һ���ɽ���Ϣ
    ///@param req_count ���󵽵��������
    ///@param trade_sequence ��ҳ����ĵ�ǰ�ر�����
    ///@param query_reference ��ǰ������Ϣ����Ӧ�Ĳ�ѯ��������Ҫ��¼�������ڽ�����һ�η�ҳ��ѯ��ʱ����Ҫ�õ�
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��trade_sequenceΪ0���������β�ѯû�в鵽�κμ�¼����is_lastΪtrueʱ�����trade_sequence����req_count����ô��ʾ���лر������Խ�����һ�η�ҳ��ѯ��������ȣ���ʾ���лر��Ѿ���ѯ��ϡ�һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ�
    virtual void OnQueryOptionCombinedTradesByPage(EMTQueryOptCombTradeRsp* trade_info, int64_t req_count, int64_t trade_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id);

    ///�����ѯ��Ȩ��ϲ��Գֲ���Ӧ
    ///@param position_info ��ѯ����һ���ֲ���Ϣ
    ///@param error_info ��ѯ�ֲַ�������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ�
    virtual void OnQueryOptionCombinedPosition(EMTQueryOptCombPositionRsp* position_info, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///�����ѯ��Ȩ��ϲ�����Ϣ��Ӧ
    ///@param strategy_info ��ѯ����һ����ϲ�����Ϣ
    ///@param error_info ��ѯ�ɽ��ر���������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ�
    virtual void OnQueryOptionCombinedStrategyInfo(EMTQueryCombineStrategyInfoRsp* strategy_info, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///��ѯ������ȯҵ���е���Ʒ�����ʵ���Ӧ
    ///@param pledge_stk_rate_info ����Ʒ��������Ϣ����ѯ��������ʱ���ؿ�
    ///@param error_info ��ѯ����Ʒ�����ʷ�������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    virtual void OnQueryCreditPledgeStkRate(EMTClientQueryCreditPledgeStkRateRsp* pledge_stk_rate_info, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///��ѯ��Ȩ��Ȩ�ϲ�ͷ�����Ӧ
    ///@param position_info ��ѯ����һ����Ȩ�ϲ�ͷ����Ϣ
    ///@param error_info ��ѯ�ֲַ�������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    virtual void OnQueryOptionCombinedExecPosition(EMTQueryOptCombExecPosRsp* position_info, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///��ѯ������ȯ��֤������Ӧ
    ///@param margin_rate_info ������ȯ��֤������Ϣ����ѯ��������ʱ���ؿ�
    ///@param error_info ��ѯ������ȯ��֤���ʷ�������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    virtual void OnQueryCreditMarginRate(EMTClientQueryCreditMarginRateRsp* margin_rate_info, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///��ѯ��ȯͷ��ȫ��ռ�÷�����Ӧ
    ///@param position_fullrate_info ��ȯͷ��ȫ��ռ�÷�����Ϣ����ѯ��������ʱ���ؿ�
    ///@param error_info ��ѯ��ȯͷ��ȫ��ռ�÷��ʷ�������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    virtual void OnQueryCreditPositionFullRate(EMTClientQueryCreditPositionFullRateRsp* position_fullrate_info, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///������ȯ�ɵ���֤ȯ��ҳ��ѯ��Ӧ
    ///@param pledge_stk_info ������ȯ�ɵ���֤ȯ��Ϣ����ѯ��������ʱ���ؿ�
    ///@param error_info ������ȯ�ɵ���֤ȯ��ҳ��ѯ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    virtual void OnQueryCreditPledgeStkPagination(EMTClientQueryCreditPledgeStkPaginationRsp* pledge_stk_info, EMTRI* error_info, int request_id, uint64_t session_id);

    ///������ȯ���֤ȯ��ҳ��ѯ��Ӧ
    ///@param target_stk_info ������ȯ���֤ȯ��Ϣ����ѯ��������ʱ���ؿ�
    ///@param error_info ������ȯ���֤ȯ��ҳ��ѯ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    virtual void OnQueryCreditTargetStkPagination(EMTClientQueryCreditTargetStkPaginationRsp* target_stk_info, EMTRI* error_info, int request_id, uint64_t session_id);

    ///�����ѯ���ҵ����Ϣ�б����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    ///@param issue_info ��ѯ���Ľ�����ɵ�һֻ��Ʊ��Ϣ
    ///@param error_info ��ѯ���������Ϣ�б�������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    virtual void OnQueryIssueInfoList(EMTQueryIssueTickerRsp* issue_info, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///�����ѯSecurity��Ϣ��Ӧ
    ///@param security ��ѯ����һֻ֤ȯ����ϸ��Ϣ
    ///@param error_info ��ѯ֤ȯ��Ϣ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark �����û����ܲ�ѯ�����Ʊ��Ϣ��һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    virtual void OnQuerySecurityInfo(EMTQuerySecurityInfoRsp* security, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///������ȯ���طֲ����ö�ȵ���֪ͨ
    ///@param quota_transfer_info ���ö�ȵ���֪ͨ�ľ�����Ϣ���û�����ͨ��quota_transfer_info.serial_id����������ͨ��GetClientIDByEMTID() == client_id�������Լ��Ķ�����
    ///@param error_info ���ö�ȵ����������ܾ����߷�������ʱ�������ʹ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark �����ö�ȵ���������״̬�仯��ʱ�򣬻ᱻ���ã���Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ����е�¼�˴��û��Ŀͻ��˶����յ����û��Ķ�ȵ���֪ͨ��
    virtual void OnCreditQuotaTransfer(EMTQuotaTransferNotice* quota_transfer_info, EMTRI* error_info, uint64_t session_id);

    ///�����ѯ������ȯ���طֲ����ö�ȵ���������Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    ///@param quota_transfer_info ���ö�ȵ���֪ͨ�ľ�����Ϣ
    ///@param error_info ��ѯ���ö�ȷ�������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    virtual void OnQueryCreditQuotaTransfer(EMTQuotaTransferNotice* quota_transfer_info, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///�����ѯ�����ʲ���Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    ///@param yesterday_asset ��ѯ���������ʲ����            
    ///@param error_info ��ѯ�����ʲ���������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    virtual void OnQueryYesterdayAsset(EMTQueryYesterdayAssetRsp* yesterday_asset, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///����Otc��ҳ�����ѯ�ֲ���Ӧ
    ///@param position_info ��ѯ����һ���ֲ���Ϣ
    ///@param req_count ���󵽵��������
    ///@param trade_sequence ��ҳ����ĵ�ǰ�ر�����
    ///@param query_reference ��ǰ������Ϣ����Ӧ�Ĳ�ѯ��������Ҫ��¼�������ڽ�����һ�η�ҳ��ѯ��ʱ����Ҫ�õ�
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��trade_sequenceΪ0���������β�ѯû�в鵽�κμ�¼����is_lastΪtrueʱ�����trade_sequence����req_count����ô��ʾ���лر������Խ�����һ�η�ҳ��ѯ��������ȣ���ʾ���лر��Ѿ���ѯ��ϡ�һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ�
    ///virtual void OnQueryOtcPositionByPage(EMTOtcPositionInfo* position_info, int64_t req_count, int64_t trade_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id);

    ///����Otc�����ѯ�ʽ��˻���Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    ///@param asset ��ѯ�����ʽ��˻����
    ///@param error_info ��ѯ�ʽ��˻���������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
    ///virtual void OnQueryOtcAsset(EMTOtcAssetInfo* asset, EMTRI* error_info, int request_id, bool is_last, uint64_t session_id);

    ///����Otc��ҳ�����ѯί����Ӧ
    ///@param order_info ��ѯ����һ������
    ///@param req_count ���󵽵��������
    ///@param order_sequence ��ҳ����ĵ�ǰ�ر�����
    ///@param query_reference ��ǰ������Ϣ����Ӧ�Ĳ�ѯ��������Ҫ��¼�������ڽ�����һ�η�ҳ��ѯ��ʱ����Ҫ�õ�
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��order_sequenceΪ0���������β�ѯû�в鵽�κμ�¼����is_lastΪtrueʱ�����order_sequence����req_count����ô��ʾ���лر������Խ�����һ�η�ҳ��ѯ��������ȣ���ʾ���лر��Ѿ���ѯ��ϡ�һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ�
    virtual void OnQueryOtcOrderByPage(EMTQueryOrderRsp* order_info, int64_t req_count, int64_t order_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id);

    ///����Otc��ҳ�����ѯ�ɽ���Ӧ
    ///@param trade_info ��ѯ����һ������
    ///@param req_count ���󵽵��������
    ///@param trade_sequence ��ҳ����ĵ�ǰ�ر�����
    ///@param query_reference ��ǰ������Ϣ����Ӧ�Ĳ�ѯ��������Ҫ��¼�������ڽ�����һ�η�ҳ��ѯ��ʱ����Ҫ�õ�
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��trade_sequenceΪ0���������β�ѯû�в鵽�κμ�¼����is_lastΪtrueʱ�����trade_sequence����req_count����ô��ʾ���лر������Խ�����һ�η�ҳ��ѯ��������ȣ���ʾ���лر��Ѿ���ѯ��ϡ�һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ�
    virtual void OnQueryOtcTradeByPage(EMTQueryTradeRsp* trade_info, int64_t req_count, int64_t trade_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id);

    ///��ҳ�����ѯETF�嵥�ļ���Ӧ
    ///@param etf_info ��ѯ����һ��ETF��Ϣ
    ///@param req_count ���󵽵��������
    ///@param rsp_sequence ��ҳ����ĵ�ǰ�ر�����
    ///@param query_reference ��ǰ��Ϣ����Ӧ�Ĳ�ѯ��������Ҫ��¼�������ڽ�����һ�η�ҳ��ѯ��ʱ����Ҫ�õ�
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��rsp_sequenceΪ0���������β�ѯû�в鵽�κμ�¼����is_lastΪtrueʱ�����rsp_sequence����req_count����ô��ʾ������Ϣ�����Խ�����һ�η�ҳ��ѯ��������ȣ���ʾ���н���Ѿ���ѯ��ϡ�һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ�
    virtual void OnQueryETFByPage(EMTQueryETFBaseRsp* etf_info, int64_t req_count, int64_t rsp_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id);

    ///��ҳ�����ѯ��Ļ�����Ϣ��Ӧ
    ///@param security_info ��ѯ����һ�������Ϣ
    ///@param req_count ���󵽵��������
    ///@param rsp_sequence ��ҳ����ĵ�ǰ�ر�����
    ///@param query_reference ��ǰ��Ϣ����Ӧ�Ĳ�ѯ��������Ҫ��¼�������ڽ�����һ�η�ҳ��ѯ��ʱ����Ҫ�õ�
    ///@param request_id ����Ϣ��Ӧ������Ӧ������ID
    ///@param is_last ����Ϣ��Ӧ�����Ƿ�Ϊrequest_id������������Ӧ�����һ����Ӧ����Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
    ///@param session_id �ʽ��˻���Ӧ��session_id����¼ʱ�õ�
    ///@remark ��rsp_sequenceΪ0���������β�ѯû�в鵽�κμ�¼����is_lastΪtrueʱ�����rsp_sequence����req_count����ô��ʾ���б��������Խ�����һ�η�ҳ��ѯ��������ȣ���ʾ���б����Ѿ���ѯ��ϡ�һ����ѯ������ܶ�Ӧ�����Ӧ����Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ�����ߡ�
    virtual void OnQuerySecurityByPage(EMTQuerySecurityByPageRsp* security_info, int64_t req_count, int64_t rsp_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id);

	//-------------------------------------------------------------------------------------
	//data���ص������������ֵ�
	//error���ص������Ĵ����ֵ�
	//-------------------------------------------------------------------------------------

    virtual void onConnected() {};

    virtual void onDisconnected(int reason) {};

    virtual void onError(const dict& error) {};

    virtual void onOrderEvent(const dict& data, const dict& error, uint64_t session_id) {};

    virtual void onTradeEvent(const dict& data, uint64_t session_id) {};

    virtual void onCancelOrderError(const dict& data, const dict& error, uint64_t session_id) {};

    virtual void onQueryOrder(const dict& data, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryOrderByPage(const dict& data, int64_t req_count, int64_t order_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryTrade(const dict& data, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryTradeByPage(const dict& data, int64_t req_count, int64_t trade_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryPosition(const dict& data, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryPositionByPage(const dict& data, int64_t req_count, int64_t trade_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryAsset(const dict& data, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryFundTransfer(const dict& data, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onFundTransfer(const dict& data, const dict& error, uint64_t session_id) {};

    virtual void onQueryOtherServerFund(const dict& data, const dict& error, int request_id, uint64_t session_id) {};

    virtual void onQueryETF(const dict& data, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryETFBasket(const dict& data, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryIPOInfoList(const dict& data, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryIPOQuotaInfo(const dict& data, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryOptionAuctionInfo(const dict& data, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onCreditCashRepay(const dict& data, const dict& error, uint64_t session_id) {};

    virtual void onCreditCashRepayDebtInterestFee(const dict& data, const dict& error, uint64_t session_id) {};

    virtual void onQueryCreditCashRepayInfo(const dict& data, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryCreditFundInfo(const dict& data, const dict& error, int request_id, uint64_t session_id) {};

    virtual void onQueryCreditDebtInfo(const dict& data, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryCreditDebtInfoByPage(const dict& data, int64_t req_count, int64_t order_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryCreditTickerDebtInfo(const dict& data, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryCreditAssetDebtInfo(double remain_amount, const dict& error, int request_id, uint64_t session_id) {};

    virtual void onQueryCreditTickerAssignInfo(const dict& data, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryCreditTickerAssignInfoByPage(const dict& data, int64_t req_count, int64_t order_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryCreditExcessStock(const dict& data, const dict& error, int request_id, uint64_t session_id) {};

    virtual void onQueryMulCreditExcessStock(const dict& data, const dict& error, int request_id, uint64_t session_id, bool is_last) {};

    virtual void onCreditExtendDebtDate(const dict& data, const dict& error, uint64_t session_id) {};

    virtual void onQueryCreditExtendDebtDateOrders(const dict& data, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryCreditFundExtraInfo(const dict& data, const dict& error, int request_id, uint64_t session_id) {};

    virtual void onQueryCreditPositionExtraInfo(const dict& data, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onOptionCombinedOrderEvent(const dict& data, const dict& error, uint64_t session_id) {};

    virtual void onOptionCombinedTradeEvent(const dict& data, uint64_t session_id) {};

    virtual void onCancelOptionCombinedOrderError(const dict& data, const dict& error, uint64_t session_id) {};

    virtual void onQueryOptionCombinedOrders(const dict& data, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryOptionCombinedOrdersByPage(const dict& data, int64_t req_count, int64_t order_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryOptionCombinedTrades(const dict& data, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryOptionCombinedTradesByPage(const dict& data, int64_t req_count, int64_t trade_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryOptionCombinedPosition(const dict& data, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryOptionCombinedStrategyInfo(const dict& data, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryCreditPledgeStkRate(const dict& data, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryOptionCombinedExecPosition(const dict& data, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryCreditMarginRate(const dict& data, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryCreditPositionFullRate(const dict& data, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryCreditPledgeStkPagination(const dict& data, const dict& error, int request_id, uint64_t session_id) {};

    virtual void onQueryCreditTargetStkPagination(const dict& data, const dict& error, int request_id, uint64_t session_id) {};

    virtual void onQueryIssueInfoList(const dict& data, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQuerySecurityInfo(const dict& data, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onCreditQuotaTransfer(const dict& data, const dict& error, uint64_t session_id) {};

    virtual void onQueryCreditQuotaTransfer(const dict& data, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryYesterdayAsset(const dict& data, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryOtcPositionByPage(EMTOtcPositionInfo position_info, int64_t req_count, int64_t trade_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryOtcAsset(EMTOtcAssetInfo asset, const dict& error, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryOtcOrderByPage(const dict& data, int64_t req_count, int64_t order_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryOtcTradeByPage(const dict& data, int64_t req_count, int64_t trade_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQueryETFByPage(const dict& data, int64_t req_count, int64_t rsp_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) {};

    virtual void onQuerySecurityByPage(const dict& data, int64_t req_count, int64_t rsp_sequence, int64_t query_reference, int request_id, bool is_last, uint64_t session_id) {};




	//-------------------------------------------------------------------------------------
	//req:���������������ֵ�
	//-------------------------------------------------------------------------------------

	void createTraderApi(int client_id, string save_file_path, int log_level);

	void release();

	void init();

	int exit();

	string getTradingDay();

	string getApiVersion();

	dict getApiLastError();

	int getClientIDByXTPID(uint64_t order_xtp_id);

	string getAccountByXTPID(uint64_t order_xtp_id);

	void subscribePublicTopic(int resume_type);

	void setSoftwareVersion(string version);

	///void setSoftwareKey(string key);

	void setHeartBeatInterval(int interval);

	uint64_t login(string ip, int port, string user, string password, int sock_type);

	int logout(uint64_t session_id);

	bool isServerRestart(uint64_t session_id);

	///int modifyUserTerminalInfo(const dict &req, uint64_t session_id);

	uint64_t insertOrder(const dict &req, uint64_t session_id);

	uint64_t cancelOrder(uint64_t order_xtp_id, uint64_t session_id);

    int queryOrderByEMTID(uint64_t order_emt_id, uint64_t session_id, int request_id);

    int queryOrders(const dict& req, uint64_t session_id, int request_id);

    int queryUnfinishedOrders(uint64_t session_id, int request_id);

    int queryOrdersByPage(const dict& req, uint64_t session_id, int request_id);

    int queryTradesByEMTID(uint64_t order_emt_id, uint64_t session_id, int request_id);

    int queryTrades(const dict& req, uint64_t session_id, int request_id);

    int queryTradesByPage(const dict& req, uint64_t session_id, int request_id);

    int queryPosition(string ticker, uint64_t session_id, int request_id, int market);

    int queryPositionByPage(const dict& req, uint64_t session_id, int request_id);

    int queryAsset(uint64_t session_id, int request_id);

    int queryFundTransfer(const dict& req, uint64_t session_id, int request_id);

    int queryOtherServerFund(const dict& req, uint64_t session_id, int request_id);

    int queryETF(const dict& req, uint64_t session_id, int request_id);

    int queryETFTickerBasket(const dict& req, uint64_t session_id, int request_id);

    int queryIPOInfoList(uint64_t session_id, int request_id);

    int queryIPOQuotaInfo(uint64_t session_id, int request_id);

    int queryOptionAuctionInfo(const dict& req, uint64_t session_id, int request_id);

    int queryCreditCashRepayInfo(uint64_t session_id, int request_id);

    int queryCreditFundInfo(uint64_t session_id, int request_id);

    int queryCreditDebtInfo(uint64_t session_id, int request_id);

    ///int queryCreditDebtInfoByPage(const dict& req, uint64_t session_id, int request_id);

    int queryCreditTickerDebtInfo(const dict& req, uint64_t session_id, int request_id);

    int queryCreditAssetDebtInfo(uint64_t session_id, int request_id);

    int queryCreditTickerAssignInfo(const dict& req, uint64_t session_id, int request_id);

    int queryCreditTickerAssignInfoByPage(const dict& req, uint64_t session_id, int request_id);

    int queryCreditExcessStock(const dict& req, uint64_t session_id, int request_id);

    int queryMulCreditExcessStock(const dict& req, uint64_t session_id, int request_id);

    int queryCreditExtendDebtDateOrders(uint64_t emt_id, uint64_t session_id, int request_id);

    int queryCreditFundExtraInfo(uint64_t session_id, int request_id);

    int queryCreditPositionExtraInfo(const dict& req, uint64_t session_id, int request_id);

    int queryOptionCombinedUnfinishedOrders(uint64_t session_id, int request_id);

    int queryOptionCombinedOrderByEMTID(uint64_t order_emt_id, uint64_t session_id, int request_id);

    int queryOptionCombinedOrders(const dict& req, uint64_t session_id, int request_id);

    int queryOptionCombinedOrdersByPage(const dict& req, uint64_t session_id, int request_id);

    int queryOptionCombinedTradesByEMTID(uint64_t order_emt_id, uint64_t session_id, int request_id);

    int queryOptionCombinedTrades(const dict& req, uint64_t session_id, int request_id);

    int queryOptionCombinedTradesByPage(const dict& req, uint64_t session_id, int request_id);

    int queryOptionCombinedPosition(const dict& req, uint64_t session_id, int request_id);

    int queryOptionCombinedStrategyInfo(uint64_t session_id, int request_id);

    int queryCreditPledgeStkRate(const dict& req, uint64_t session_id, int request_id);

    int queryOptionCombinedExecPosition(const dict& req, uint64_t session_id, int request_id);

    int queryCreditMarginRate(const dict& req, uint64_t session_id, int request_id);

    int queryCreditPositionFullRate(const dict& req, uint64_t session_id, int request_id);

    int queryCreditPledgeStkPagination(const dict& req, uint64_t session_id, int request_id);

    int queryCreditTargetStkPagination(const dict& req, uint64_t session_id, int request_id);

    int queryIssueInfoList(uint64_t session_id, int request_id);

    int querySecurityInfo(const dict& req, uint64_t session_id, int request_id);

    int queryCreditQuotaTransfer(const dict& req, uint64_t session_id, int request_id);

    int queryYesterdayAsset(uint64_t session_id, int request_id);

    int queryOtcPositionByPage(const dict& req, uint64_t session_id, int request_id);

    int queryOtcAsset(uint64_t session_id, int request_id);

    int queryOtcOrdersByPage(const dict& req, uint64_t session_id, int request_id);

    int queryOtcTradesByPage(const dict& req, uint64_t session_id, int request_id);

    int queryETFByPage(const dict& req, uint64_t session_id, int request_id);

    int querySecurityByPage(const dict& req, uint64_t session_id, int request_id);

};
