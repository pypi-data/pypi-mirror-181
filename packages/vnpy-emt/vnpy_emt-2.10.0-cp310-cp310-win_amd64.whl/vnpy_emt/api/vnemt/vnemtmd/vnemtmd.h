//ϵͳ
#ifdef WIN32
//#include "stdafx.h"
#endif

#include "vnemt.h"
#include "pybind11/pybind11.h"
#include "emt/emt_quote_api.h"


using namespace pybind11;
using namespace EMT::API;


///-------------------------------------------------------------------------------------
///C++ SPI�Ļص���������ʵ��
///-------------------------------------------------------------------------------------

//API�ļ̳�ʵ��
class MdApi : public QuoteSpi
{
private:
	QuoteApi* api = NULL;				//API����
	bool active = false;		//����״̬

public:
	MdApi()
	{
	};

	~MdApi()
	{
		if (this->active)
		{
			this->exit();
		}
	};

	//-------------------------------------------------------------------------------------
	//API�ص�����
	//-------------------------------------------------------------------------------------

	///���ͻ����������̨ͨ�����ӶϿ�ʱ���÷��������á�
	///@param reason ����ԭ��������������Ӧ
	///@remark api�����Զ������������߷���ʱ�����û�����ѡ����������������ڴ˺����е���Login���µ�¼��ע���û����µ�¼����Ҫ���¶�������
	virtual void OnDisconnected(int reason);

	/**
	*   ����Ӧ��
	*   @attention					�˺���ֻ���ڷ�������������ʱ�Ż���ã�һ�������û�����
	*   @param error_info			����������Ӧ��������ʱ�ľ����������
	*   @return						�ú�������Ϊvoid
	*/
	virtual void OnError(EMTRspInfoStruct* error_info);

	/**
	*   ָ������֪ͨ
	*   @attention					��Ҫ���ٷ��أ���������������Ϣ��������ʱ������������ʱ���ᴥ������
	*   @param index_data			ָ���������ݣ�ֻ��ָ��������������ֶ�
	*/
	virtual void OnIndexData(EMTIndexDataStruct* index_data);

	/**
	*   �������֪ͨ��������һ��һ����
	*   @attention					��Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
	*   @param market_data			��������
	*   @param bid1_qty				��һ��������
	*   @param bid1_count			��һ���е���Чί�б���
	*   @param max_bid1_count		��һ������ί�б���
	*   @param ask1_qty				��һ��������
	*   @param ask1_count			��һ���е���Чί�б���
	*   @param max_ask1_count		��һ������ί�б���
	*/
	virtual void OnDepthMarketData(EMTMarketDataStruct* market_data, int64_t bid1_qty[], int32_t bid1_count, int32_t max_bid1_count, int64_t ask1_qty[], int32_t ask1_count, int32_t max_ask1_count);

	/**
	*   �������֪ͨ��������Ʊ������Ȩ֤��ծȯ����Ѻʽ�ع�
	*   @attention					ÿ�����ĵĺ�Լ����Ӧһ������Ӧ����Ҫ���ٷ��أ����������������Ϣ������������ʱ���ᴥ������
	*   @param tbt_data				����������ݣ��������ί�к���ʳɽ�����Ϊ���ýṹ�壬��Ҫ����type�����������ί�л�����ʳɽ�
	*/
	virtual void OnTickByTick(EMTTickByTickStruct* tbt_data);

	/**
	*   ���鶩����֪ͨ
	*   @param order_book			���鶩�������ݣ���Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
	*/
	virtual void OnOrderBook(EMTOrderBookStruct* order_book);

	/**
	*   ��ʱ����֪ͨ
	*   @param minute_info			��ʱ�������ݣ���Ҫ���ٷ��أ���������������Ϣ������������ʱ���ᴥ������
	*/
	virtual void OnMinuteInfo(EMTMinuteInfo* minute_info);

	/**
	*   ����ȫ�г���ָ������Ӧ��
	*   @attention					��Ҫ���ٷ���
	*   @param exchange_id			���������룬EMT_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���EMT_EXCHANGE_SZ��ʾΪ����ȫ�г�
	*	@param error_info			���ĺ�Լʱ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
	*/
	virtual void OnSubscribeAllIndexData(EMT_EXCHANGE_TYPE exchange_id, EMTRspInfoStruct* error_info);

	/**
	*   �˶�ȫ�г���ָ������Ӧ��
	*   @attention					��Ҫ���ٷ���
	*   @param exchange_id			���������룬EMT_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���EMT_EXCHANGE_SZ��ʾΪ����ȫ�г�
	*	@param error_info			ȡ�����ĺ�Լʱ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
	*/
	virtual void OnUnSubscribeAllIndexData(EMT_EXCHANGE_TYPE exchange_id, EMTRspInfoStruct* error_info);

	/**
	*   ����ָ������Ӧ��
	*   @attention					ÿ�����ĵĺ�Լ��Ӧһ������Ӧ����Ҫ���ٷ��أ����������������Ϣ������������ʱ���ᴥ������
	*   @param ticker				���ĵĺ�Լ��Ŵ���
	*   @param error_info			���ĺ�Լ��������ʱ�Ĵ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
	*	@param is_last				�Ƿ�˴ζ��ĵ����һ��Ӧ�𣬵�Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
	*/
	virtual void OnSubIndexData(EMTSpecificTickerStruct* ticker, EMTRspInfoStruct* error_info, bool is_last);

	/**
	*   �˶�ָ������Ӧ��
	*   @attention					ÿ�����ĵĺ�Լ��Ӧһ���˶�Ӧ����Ҫ���ٷ��أ����������������Ϣ������������ʱ���ᴥ������
	*   @param ticker				���ĵĺ�Լ��Ŵ���
	*   @param error_info			ȡ�����ĺ�Լ��������ʱ�Ĵ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
	*	@param is_last				�Ƿ�˴�ȡ�����ĵ����һ��Ӧ�𣬵�Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
	*/
	virtual void OnUnSubIndexData(EMTSpecificTickerStruct* ticker, EMTRspInfoStruct* error_info, bool is_last);

	/**
	*   ����ȫ�г���Ʊ��������Ӧ��
	*   @attention					��Ҫ���ٷ���
	*   @param exchange_id			���������룬EMT_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���EMT_EXCHANGE_SZ��ʾΪ����ȫ�г�
	*	@param error_info			���ĺ�Լ��������ʱ�Ĵ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
	*/
	virtual void OnSubscribeAllMarketData(EMT_EXCHANGE_TYPE exchange_id, EMTRspInfoStruct* error_info);

	/**
	*   �˶�ȫ�г��Ĺ�Ʊ��������Ӧ��
	*   @attention					��Ҫ���ٷ���
	*   @param exchange_id			���������룬EMT_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���EMT_EXCHANGE_SZ��ʾΪ����ȫ�г�
	*	@param error_info			ȡ�����ĺ�Լʱ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
	*/
	virtual void OnUnSubscribeAllMarketData(EMT_EXCHANGE_TYPE exchange_id, EMTRspInfoStruct* error_info);

	/**
	*   ���Ŀ�������Ӧ�𣬰�����Ʊ������ծȯ��Ȩ֤����Ѻʽ�ع�
	*   @attention					ÿ�����ĵĺ�Լ��Ӧһ������Ӧ����Ҫ���ٷ��أ����������������Ϣ������������ʱ���ᴥ������
	*   @param ticker				���ĵĺ�Լ��Ŵ���
	*   @param error_info			���ĺ�Լ��������ʱ�Ĵ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
	*	@param is_last				�Ƿ�˴ζ��ĵ����һ��Ӧ�𣬵�Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
	*/
	virtual void OnSubMarketData(EMTSpecificTickerStruct* ticker, EMTRspInfoStruct* error_info, bool is_last);

	/**
	*   �˶���������Ӧ�𣬰�����Ʊ������ծȯ��Ȩ֤����Ѻʽ�ع�
	*   @attention					ÿ�����ĵĺ�Լ��Ӧһ������Ӧ����Ҫ���ٷ��أ����������������Ϣ������������ʱ���ᴥ������
	*   @param ticker				���ĵĺ�Լ��Ŵ���
	*   @param error_info			ȡ�����ĺ�Լ��������ʱ�Ĵ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
	*	@param is_last				�Ƿ�˴�ȡ�����ĵ����һ��Ӧ�𣬵�Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
	*/
	virtual void OnUnSubMarketData(EMTSpecificTickerStruct* ticker, EMTRspInfoStruct* error_info, bool is_last);

	/**
	*   ����ȫ�г����������Ӧ��
	*   @attention					��Ҫ���ٷ���
	*   @param exchange_id			���������룬EMT_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���EMT_EXCHANGE_SZ��ʾΪ����ȫ�г�
	*	@param error_info			���ĺ�Լʱ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
	*/
	virtual void OnSubscribeAllTickByTick(EMT_EXCHANGE_TYPE exchange_id, EMTRspInfoStruct* error_info);

	/**
	*   �˶�ȫ�г����������Ӧ��
	*   @attention					��Ҫ���ٷ���
	*   @param exchange_id			���������룬EMT_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���EMT_EXCHANGE_SZ��ʾΪ����ȫ�г�
	*	@param error_info			ȡ�����ĺ�Լʱ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
	*/
	virtual void OnUnSubscribeAllTickByTick(EMT_EXCHANGE_TYPE exchange_id, EMTRspInfoStruct* error_info);

	/**
	*   �����������Ӧ�𣬰�����Ʊ������ծȯ��Ȩ֤
	*   @attention					ÿ�����ĵĺ�Լ����Ӧһ������Ӧ����Ҫ���ٷ��أ����������������Ϣ������������ʱ���ᴥ������
	*   @param ticker				���ĵĺ�Լ������
	*   @param error_info			���ĺ�Լ��������ʱ�Ĵ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
	*	@param is_last				�Ƿ�˴ζ��ĵ����һ��Ӧ�𣬵�Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
	*/
	virtual void OnSubTickByTick(EMTSpecificTickerStruct* ticker, EMTRspInfoStruct* error_info, bool is_last);

	/**
	*   �˶��������Ӧ�𣬰�����Ʊ������ծȯ��Ȩ֤
	*   @attention					ÿ�����ĵĺ�Լ����Ӧһ������Ӧ����Ҫ���ٷ��أ����������������Ϣ������������ʱ���ᴥ������
	*   @param ticker				���ĵĺ�Լ������
	*   @param error_info			ȡ�����ĺ�Լʱ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
	*	@param is_last				�Ƿ�˴�ȡ�����ĵ����һ��Ӧ�𣬵�Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
	*/
	virtual void OnUnSubTickByTick(EMTSpecificTickerStruct* ticker, EMTRspInfoStruct* error_info, bool is_last);

	/**
	*   �������鶩����Ӧ��
	*   @attention                  ��Ҫ���ٷ���
	*   @param exchange_id          ���������룬EMT_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���EMT_EXCHANGE_SZ��ʾΪ����ȫ�г�
	*   @param error_info           ���ĺ�Լʱ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���*/
	virtual void OnSubscribeAllOrderBook(EMT_EXCHANGE_TYPE exchange_id, EMTRspInfoStruct* error_info);

	/**
	*   �˶�ȫ�г��Ĺ�Ʊ���鶩����Ӧ��
	*   @attention                  ��Ҫ���ٷ���
	*   @param exchange_id          ���������룬EMT_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���EMT_EXCHANGE_SZ��ʾΪ����ȫ�г�
	*   @param error_info           ȡ�����ĺ�Լʱ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
	*/
	virtual void OnUnSubscribeAllOrderBook(EMT_EXCHANGE_TYPE exchange_id, EMTRspInfoStruct* error_info);

	/**
	*   �������鶩����Ӧ��
	*   @attention                  ��Ҫ���ٷ���
	*   @param ticker               ���ĵĺ�Լ������
	*   @param error_info           ���ĺ�Լ��������ʱ�Ĵ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
	*   @param is_last              �Ƿ�˴ζ��ĵ����һ��Ӧ�𣬵�Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
	*/
	virtual void OnSubOrderBook(EMTSpecificTickerStruct* ticker, EMTRspInfoStruct* error_info, bool is_last);

	/**
	*   �˶����鶩����Ӧ��
	*   @attention                  ��Ҫ���ٷ���
	*   @param ticker               ���ĵĺ�Լ��Ŵ���
	*   @param error_info           ȡ�����ĺ�Լ��������ʱ�Ĵ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
	*   @param is_last              �Ƿ�˴ζ��ĵ����һ��Ӧ�𣬵�Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
	*/
	virtual void OnUnSubOrderBook(EMTSpecificTickerStruct* ticker, EMTRspInfoStruct* error_info, bool is_last);

	/**
	*   ����ȫ�г���ʱ����
	*   @attention                  ��Ҫ���ٷ���
	*   @param exchange_id          ���������룬EMT_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���EMT_EXCHANGE_SZ��ʾΪ����ȫ�г�
	*   @param error_info           ���ĺ�Լʱ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
	*/
	virtual void OnSubscribeAllMinuteInfo(EMT_EXCHANGE_TYPE exchange_id, EMTRspInfoStruct* error_info);

	/**
	*   �˶�ȫ�г���ʱ����
	*   @attention                  ��Ҫ���ٷ���
	*   @param exchange_id          ���������룬EMT_EXCHANGE_SH��ʾΪ�Ϻ�ȫ�г���EMT_EXCHANGE_SZ��ʾΪ����ȫ�г�
	*   @param error_info           ȡ�����ĺ�Լʱ��������ʱ���صĴ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
	*/
	virtual void OnUnSubscribeAllMinuteInfo(EMT_EXCHANGE_TYPE exchange_id, EMTRspInfoStruct* error_info);

	/**
	*   ���ķ�ʱ����
	*   @attention                  ��Ҫ���ٷ���
	*   @param ticker               ���ĵĺ�Լ������
	*   @param error_info           ���ĺ�Լ��������ʱ�Ĵ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
	*   @param is_last              �Ƿ�˴ζ��ĵ����һ��Ӧ�𣬵�Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
	*/
	virtual void OnSubMinuteInfo(EMTSpecificTickerStruct* ticker, EMTRspInfoStruct* error_info, bool is_last);

	/**
	*   �˶���ʱ����
	*   @attention                  ��Ҫ���ٷ���
	*   @param ticker               ���ĵĺ�Լ������
	*   @param error_info           ���ĺ�Լ��������ʱ�Ĵ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
	*   @param is_last              �Ƿ�˴�ȡ�����ĵ����һ��Ӧ�𣬵�Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
	*/
	virtual void OnUnSubMinuteInfo(EMTSpecificTickerStruct* ticker, EMTRspInfoStruct* error_info, bool is_last);

	/**
	*   ��ѯȫ�г���Լ���־�̬��Ϣ��Ӧ��
	*   @attention					��Ҫʹ�ú�Լ���־�̬��Ϣ�ṹ��EMTQuoteStaticInfo
	*   @param qsi					��Լ���־�̬��Ϣ�ṹ��
	*   @param error_info			���ĺ�Լ��������ʱ�Ĵ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
	*   @param is_last				�Ƿ�˴��˶������һ��Ӧ�𣬵�Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
	*/
	virtual void OnQueryAllTickers(EMTQuoteStaticInfo* qsi, EMTRspInfoStruct* error_info, bool is_last);

	/**
	*   ��ѯȫ�г���Լ������̬��Ϣ��Ӧ��
	*   @attention					��Ҫʹ�ú�Լ������̬��Ϣ�ṹ��EMTQutoFullInfo
	*   @param qfi					��Լ������̬��Ϣ�ṹ��
	*   @param error_info			���ĺ�Լ��������ʱ�Ĵ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
	*   @param is_last				�Ƿ�˴��˶������һ��Ӧ�𣬵�Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
	*/
	virtual void OnQueryAllTickersFullInfo(EMTQuoteFullInfo* qfi, EMTRspInfoStruct* error_info, bool is_last);

	/**
	*   ��ѯ��Լ����ָ����Ӧ��
	*   @attention					��Ҫʹ���������ݽṹ��EMTIndexDataStruct
	*   @param index_data			����ָ������
	*   @param error_info			���ĺ�Լ��������ʱ�Ĵ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
	*   @param is_last				�Ƿ�˴��˶������һ��Ӧ�𣬵�Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
	*/
	virtual void OnQueryLatestIndexData(EMTIndexDataStruct* index_data, EMTRspInfoStruct* error_info, bool is_last);

	/**
	*   ��ѯ��Լ�����ֻ����յ�Ӧ��
	*   @attention					��Ҫʹ���������ݽṹ��EMTIndexDataStruct
	*   @param market_data			�����ֻ���������
	*   @param error_info			���ĺ�Լ��������ʱ�Ĵ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
	*   @param is_last				�Ƿ�˴��˶������һ��Ӧ�𣬵�Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
	*/
	virtual void OnQueryLatestMarketData(EMTMarketDataStruct* market_data, EMTRspInfoStruct* error_info, bool is_last);

	/**
	*   ��ѯ��ʱ���ݵ�Ӧ��
	*   @attention					��Ҫʹ�÷�ʱ�ṹ��EMTMinuteInfo
	*   @param minute_info			���·�ʱ����
	*   @param error_info			���ĺ�Լ��������ʱ�Ĵ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
	*   @param is_last				�Ƿ�˴��˶������һ��Ӧ�𣬵�Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
	*/
	virtual void OnQueryMinuteInfo(EMTMinuteInfo* minute_info, EMTRspInfoStruct* error_info, bool is_last);

	/**
	*   ��ѯ��ʷ��ʱ���ݵ�Ӧ��
	*   @attention					��Ҫʹ�÷�ʱ�ṹ��EMTMinuteInfo
	*   @param minute_info			��ʷ��ʱ����
	*   @param error_info			���ĺ�Լ��������ʱ�Ĵ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
	*   @param is_last				�Ƿ�˴��˶������һ��Ӧ�𣬵�Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
	*/
	virtual void OnQueryMinHistoryInfo(EMTMinuteInfo* minute_info, EMTRspInfoStruct* error_info, bool is_last);

	/*
	* ��ѯ���¼�
	* @attention					��Ҫʹ�����¼۽ṹ��EMTTickerPriceInfo
	* @param price_info				���¼۸�����
	* @param error_info				���ĺ�Լ��������ʱ�Ĵ�����Ϣ����error_infoΪ�գ�����error_info.error_idΪ0ʱ������û�д���
	* @param is_last				�Ƿ�˴��˶������һ��Ӧ�𣬵�Ϊ���һ����ʱ��Ϊtrue�����Ϊfalse����ʾ��������������Ϣ��Ӧ
	*/
	virtual void OnQueryTickersPriceInfo(EMTTickerPriceInfo* price_info, EMTRspInfoStruct* error_info, bool is_last);

	//-------------------------------------------------------------------------------------
	//data���ص������������ֵ�
	//error���ص������Ĵ����ֵ�
	//������������ԭ����
	//-------------------------------------------------------------------------------------

	virtual void onDisconnected(int reason) {};

	virtual void onError(const dict& data) {};

	virtual void onIndexData(const dict& data) {};

	virtual void onDepthMarketData(const dict& data) {};

	virtual void onTickByTick(const dict& data) {};

	virtual void onOrderBook(const dict& data) {};

	virtual void onMinuteInfo(const dict& data) {};

	virtual void onSubscribeAllIndexData(int exchange_id, const dict& data) {};

	virtual void onUnSubscribeAllIndexData(int exchange_id, const dict& data) {};

	virtual void onSubIndexData(const dict& data, const dict& error, bool is_last) {};

	virtual void onUnSubIndexData(const dict& data, const dict& error, bool is_last) {};

	virtual void onSubscribeAllMarketData(int exchange_id, const dict& data) {};

	virtual void onUnSubscribeAllMarketData(int exchange_id, const dict& data) {};

	virtual void onSubMarketData(const dict& data, const dict& error, bool is_last) {};

	virtual void onUnSubMarketData(const dict& data, const dict& error, bool is_last) {};

	virtual void onSubscribeAllTickByTick(int exchange_id, const dict& data) {};

	virtual void onUnSubscribeAllTickByTick(int exchange_id, const dict& data) {};

	virtual void onSubTickByTick(const dict& data, const dict& error, bool is_last) {};

	virtual void onUnSubTickByTick(const dict& data, const dict& error, bool is_last) {};

	virtual void onSubscribeAllOrderBook(int exchange_id, const dict& data) {};

	virtual void onUnSubscribeAllOrderBook(int exchange_id, const dict& data) {};

	virtual void onSubOrderBook(const dict& data, const dict& error, bool is_last) {};

	virtual void onUnSubOrderBook(const dict& data, const dict& error, bool is_last) {};

	virtual void onSubscribeAllMinuteInfo(int exchange_id, const dict& data) {};

	virtual void onUnSubscribeAllMinuteInfo(int exchange_id, const dict& data) {};

	virtual void onSubMinuteInfo(const dict& data, const dict& error, bool is_last) {};

	virtual void onUnSubMinuteInfo(const dict& data, const dict& error, bool is_last) {};

	virtual void onQueryAllTickers(const dict& data, const dict& error, bool is_last) {};

	virtual void onQueryAllTickersFullInfo(const dict& data, const dict& error, bool is_last) {};

	virtual void onQueryLatestIndexData(const dict& data, const dict& error, bool is_last) {};

	virtual void onQueryLatestMarketData(const dict& data, const dict& error, bool is_last) {};

	virtual void onQueryMinuteInfo(const dict& data, const dict& error, bool is_last) {};

	virtual void onQueryMinHistoryInfo(const dict& data, const dict& error, bool is_last) {};

	virtual void onQueryTickersPriceInfo(const dict& data, const dict& error, bool is_last) {};


	//-------------------------------------------------------------------------------------
	//req:���������������ֵ�
	//-------------------------------------------------------------------------------------

	void createQuoteApi(int client_id, string save_file_path, int data_type, int log_level);

	void release();

	void init();

	int exit();

	//string getTradingDay();��������ڽ���API����

	string getApiVersion();

	dict getApiLastError();

	void setUDPBufferSize(int buff_size);

	void setHeartBeatInterval(int interval);

	int subscribeMarketData(string ticker, int count, int exchange_id);

	int unSubscribeMarketData(string ticker, int count, int exchange_id);

	int subscribeOrderBook(string ticker, int count, int exchange_id);

	int unSubscribeOrderBook(string ticker, int count, int exchange_id);

	int subscribeTickByTick(string ticker, int count, int exchange_id);

	int unSubscribeTickByTick(string ticker, int count, int exchange_id);

	int subscribeAllMarketData(int exchange_id);

	int unSubscribeAllMarketData(int exchange_id);

	int subscribeAllOrderBook(int exchange_id);

	int unSubscribeAllOrderBook(int exchange_id);

	int subscribeAllTickByTick(int exchange_id);

	int unSubscribeAllTickByTick(int exchange_id);

	int login(string ip, int port, string user, string password, int sock_type, string local_ip);

	int logout();

	int queryAllTickers(int exchange_id);

	int queryAllTickersFullInfo(int exchange_id);

	int queryLatestInfo(string ticker, int ticker_type, int exchange_id);

	int queryMinuteInfo(string tickers, int count, int ticker_type, int exchange_id);

	int queryMinHistoryInfo(string tickers, int count, int datetime, int ticker_type, int exchange_id);

	int queryTickersPriceInfo(string tickers, int count, int exchange_id);


};
