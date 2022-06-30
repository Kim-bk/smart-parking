package com.smartparking.service.impl;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.smartparking.dto.CustomerDTO;
import com.smartparking.entity.AddressEntity;
import com.smartparking.entity.CustomerEntity;
import com.smartparking.mapper.CustomerMapper;
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
	
	@Autowired
	private CustomerMapper mapper;
	

	@Override
	public void save(CustomerDTO customer) {
		CustomerEntity customer1 = new CustomerEntity();
		customer1.setEmail(customer.getEmail());
		customer1.setName(customer.getName());
		customer1.setNumberPhone(customer.getNumberPhone());
		List<CustomerEntity> list = repository.findAll();
		int leng = list.size()+10;
		customer1.setId("KH"+leng);
		customer1.setCustomerCard("00000");

		
		AddressEntity address = new AddressEntity();
		address.setProvinceAddress((provinceRepo.findById(customer.getIdProvince())).get());
		address.setDistrictAddress((districtRepo.findById(customer.getIdDistrict())).get());
		address.setWardAddress((wardRepo.findById(customer.getIdWard())).get());
		address.setSpecificAddress(customer.getSpecificAddress());
		customer1.setAddress(address);
		
		
		repository.save(customer1); 
	}



	@Override
	public List<CustomerDTO> findAll() {
		List<CustomerEntity> list = repository.findAll();
		List<CustomerDTO> output = new ArrayList<CustomerDTO>();
		
		for (CustomerEntity item:list) {
			CustomerDTO dto = mapper.toDTO(item);
			output.add(dto);
		}
		return output;
	}



	@Override
	public void update(String id, String customerCard) {
		Optional<CustomerEntity> customer = repository.findById(id);
		if (customer.isPresent()) {
			customer.get().setCustomerCard(customerCard);		
			repository.save(customer.get());
		}
	}



	@Override
	public List<CustomerEntity> findByCustomerCardNot(String customerCard) {
		List<CustomerEntity> list = repository.findByCustomerCard(customerCard);
		return list;
	}



	@Override
	public CustomerEntity findByEmailAndPassword(String email) {
		List<CustomerEntity> lst = repository.findByEmail(email);
		return lst.isEmpty()?null:lst.get(0);
	}
	
	

}
