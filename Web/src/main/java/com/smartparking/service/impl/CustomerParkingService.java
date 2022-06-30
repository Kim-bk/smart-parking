package com.smartparking.service.impl;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.smartparking.entity.CustomerEntity;
import com.smartparking.entity.CustomerParkingEntity;
import com.smartparking.repository.CustomerParkingRepository;
import com.smartparking.service.ICustomerParkingService;

@Service
public class CustomerParkingService implements ICustomerParkingService{
	
	@Autowired
	private CustomerParkingRepository repository;

	@Override
	public List<CustomerParkingEntity> findAll() {
		List<CustomerParkingEntity> list = repository.findAll();
		return list;
	}

	@Override
	public List<CustomerParkingEntity> findByCustomer(CustomerEntity customer) {
		List<CustomerParkingEntity> lst = repository.findAll();
		List<CustomerParkingEntity> results = new ArrayList<CustomerParkingEntity>();
		for (CustomerParkingEntity item : lst) {
				if (item.getCustomer().getCustomerCard().equals(customer.getCustomerCard())) {
					results.add(item);
				}

			
		}
		return results;
	}

}
