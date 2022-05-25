package com.smartparking.service.impl;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.smartparking.dto.WardDTO;
import com.smartparking.entity.WardEntity;
import com.smartparking.mapper.WardMapper;
import com.smartparking.repository.WardRepository;
import com.smartparking.service.IWardService;


@Service
public class WardService implements IWardService{

	@Autowired
	private WardRepository repository;
	
	@Autowired
	private WardMapper mapper;
	
	
	
	
	@Override
	public List<WardDTO> findByDistrict(String id) {
		List<WardDTO> list = new ArrayList<WardDTO>();
		
			List<WardEntity> wards = repository.findByIdDistrict(id);
			for (WardEntity item:wards) {
				list.add(mapper.toDTO(item));
			}
		
		return list.isEmpty()?null:list;
	}

	@Override
	public WardDTO findOneById(String id) {
		Optional<WardEntity> ward = repository.findById(id);
		if (ward.isPresent()) {
			WardDTO dto = mapper.toDTO(ward.get());
			return dto;
		}
		return null;
	}

}
