package com.smartparking.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.smartparking.dto.CustomerDTO;
import com.smartparking.entity.AddressEntity;
import com.smartparking.entity.CustomerEntity;
import com.smartparking.repository.CustomerRepository;
import com.smartparking.repository.DistrictRepository;
import com.smartparking.repository.ProvinceRepository;
import com.smartparking.repository.WardRepository;
import com.smartparking.service.ICustomerService;


@Service
public class CustomerService implements ICustomerService{
	
	@Autowired
	private CustomerRepository repository;
	
	@Autowired 
	private ProvinceRepository provinceRepo;
	
	@Autowired 
	private DistrictRepository districtRepo;
	
	@Autowired 
	private WardRepository wardRepo;
	
	

	@Override
	public void save(CustomerDTO customer) {
		CustomerEntity customer1 = new CustomerEntity();
		customer1.setEmail(customer.getEmail());
		customer1.setName(customer.getName());
		customer1.setNumberPhone(customer.getNumberPhone());
		customer1.setId("KH03");
		customer1.setCustomerCard("A123F800");

		
		AddressEntity address = new AddressEntity();
		address.setProvinceAddress((provinceRepo.findById(customer.getIdProvince())).get());
		address.setDistrictAddress((districtRepo.findById(customer.getIdDistrict())).get());
		address.setWardAddress((wardRepo.findById(customer.getIdWard())).get());
		address.setSpecificAddress(customer.getSpecificAddress());
		customer1.setAddress(address);

		repository.save(customer1); 
	}

}
